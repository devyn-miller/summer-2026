"""Core orchestration + Notion API interactions."""

from __future__ import annotations

import time
from typing import Any

from notion_client import APIResponseError, Client

from config import Settings
from notion_helpers import (
    append_blocks,
    bulleted_block,
    callout_block,
    divider_block,
    heading_block,
    paragraph_block,
    rich_text,
    select_option,
    todo_block,
)
from sample_data import (
    ACTIVITIES_ENTRIES,
    AVAILABILITY_CONFLICTS_MAP,
    BUDGET_ENTRIES,
    BUCKET_LIST_ENTRIES,
    HIGHLIGHTS_ENTRIES,
    MASTER_CALENDAR_ENTRIES,
    PLACES_ENTRIES,
)


def format_api_error(exc: APIResponseError) -> str:
    """Return a stable error string across notion-client versions."""
    code = getattr(exc, "code", "unknown_error")
    return f"{code}: {exc}"


class SummerPlannerBuilder:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.notion = Client(auth=settings.notion_token)

    def create_main_page(self) -> str:
        print("Creating main page: Summer 2026 Planner ...")
        response = self.notion.pages.create(
            parent={"type": "page_id", "page_id": self.settings.parent_page_id},
            icon={"type": "emoji", "emoji": "🌞"},
            cover={"type": "external", "external": {"url": self.settings.cover_image_url}},
            properties={"title": {"title": rich_text("Summer 2026 Planner 🦆")}},
        )
        page_id = response["id"]
        print(f"  ✓ Main page created - ID: {page_id}")
        return page_id

    def create_master_calendar(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Master Calendar 🕓"),
            icon={"type": "emoji", "emoji": "📅"},
            is_inline=True,
            properties={
                "Name": {"title": {}},
                "Date Range": {"date": {}},
                "Status": {
                    "select": {
                        "options": [
                            select_option("Planned", "blue"),
                            select_option("Booked", "green"),
                            select_option("Done", "gray"),
                        ]
                    }
                },
                "Assigned To": {"people": {}},
                "Notes": {"rich_text": {}},
            },
        )
        return db["id"]

    def seed_master_calendar(self, db_id: str) -> None:
        for name, start, end, status in MASTER_CALENDAR_ENTRIES:
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Name": {"title": rich_text(name)},
                    "Date Range": {"date": {"start": start, "end": end}},
                    "Status": {"select": {"name": status}},
                },
            )
        print(f"  ✓ Seeded {len(MASTER_CALENDAR_ENTRIES)} calendar entries.")

    def create_activities_db(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Activities 🔥"),
            icon={"type": "emoji", "emoji": "🏃"},
            is_inline=True,
            properties={
                "Activity Name": {"title": {}},
                "Type": {
                    "select": {
                        "options": [
                            select_option("Outdoor", "green"),
                            select_option("Indoor", "blue"),
                            select_option("Event", "purple"),
                            select_option("Relax", "yellow"),
                        ]
                    }
                },
                "Duration": {"number": {"format": "number"}},
                "Cost": {"number": {"format": "dollar"}},
                "Status": {
                    "select": {
                        "options": [
                            select_option("Planned", "blue"),
                            select_option("In Progress", "yellow"),
                            select_option("Done", "green"),
                        ]
                    }
                },
                "Energy": {
                    "select": {
                        "options": [
                            select_option("Low", "green"),
                            select_option("Medium", "yellow"),
                            select_option("High", "red"),
                        ]
                    }
                },
                "Weather": {
                    "select": {
                        "options": [
                            select_option("Hot day", "orange"),
                            select_option("Cool evening", "blue"),
                            select_option("Any", "gray"),
                        ]
                    }
                },
                "People": {
                    "multi_select": {
                        "options": [
                            select_option("Solo", "gray"),
                            select_option("You + BF", "pink"),
                            select_option("Friends", "purple"),
                            select_option("Family", "green"),
                        ]
                    }
                },
            },
        )
        return db["id"]

    def seed_activities(self, db_id: str) -> None:
        for name, atype, dur, cost, status, energy, weather, people in ACTIVITIES_ENTRIES:
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Activity Name": {"title": rich_text(name)},
                    "Type": {"select": {"name": atype}},
                    "Duration": {"number": dur},
                    "Cost": {"number": cost},
                    "Status": {"select": {"name": status}},
                    "Energy": {"select": {"name": energy}},
                    "Weather": {"select": {"name": weather}},
                    "People": {"multi_select": [{"name": p} for p in people]},
                },
            )
        print(f"  ✓ Seeded {len(ACTIVITIES_ENTRIES)} activity entries.")

    def create_availability_db(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Availability 4️⃣"),
            icon={"type": "emoji", "emoji": "📆"},
            is_inline=True,
            properties={
                "Week": {
                    "select": {
                        "options": [
                            select_option("Typical Week", "blue"),
                            select_option("Week with Overtime", "yellow"),
                        ]
                    }
                },
                "Person": {
                    "select": {
                        "options": [
                            select_option("You", "green"),
                            select_option("BF (TBD)", "purple"),
                        ]
                    }
                },
                "Free Slots": {
                    "multi_select": {
                        "options": [
                            select_option("Mon-Thu After Work", "yellow"),
                            select_option("Fri After Work", "yellow"),
                            select_option("Saturday", "green"),
                            select_option("Sunday", "blue"),
                        ]
                    }
                },
                "Conflicts": {"rich_text": {}},
            },
        )
        return db["id"]

    def seed_availability(self, db_id: str) -> None:
        for (week, person), (conflict, slots) in AVAILABILITY_CONFLICTS_MAP.items():
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Week": {"select": {"name": week}},
                    "Person": {"select": {"name": person}},
                    "Free Slots": {"multi_select": [{"name": s} for s in slots]},
                    "Conflicts": {"rich_text": rich_text(conflict) if conflict else []},
                },
            )
        print(f"  ✓ Seeded {len(AVAILABILITY_CONFLICTS_MAP)} availability entries.")

    def create_places_db(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Places to Go 🦮"),
            icon={"type": "emoji", "emoji": "📍"},
            is_inline=True,
            properties={
                "Name": {"title": {}},
                "Location": {"rich_text": {}},
                "Type": {
                    "select": {
                        "options": [
                            select_option("Beach", "blue"),
                            select_option("Park", "green"),
                            select_option("City", "purple"),
                            select_option("Trail", "brown"),
                            select_option("Cafe", "orange"),
                            select_option("Other", "gray"),
                        ]
                    }
                },
                "Distance": {"number": {"format": "number"}},
                "Cost": {"number": {"format": "dollar"}},
                "Link": {"url": {}},
                "Rating": {"number": {"format": "number"}},
            },
        )
        return db["id"]

    def seed_places(self, db_id: str) -> None:
        for name, loc, ptype, dist, cost, link, rating in PLACES_ENTRIES:
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Name": {"title": rich_text(name)},
                    "Location": {"rich_text": rich_text(loc)},
                    "Type": {"select": {"name": ptype}},
                    "Distance": {"number": dist},
                    "Cost": {"number": cost},
                    "Link": {"url": link},
                    "Rating": {"number": rating},
                },
            )
        print(f"  ✓ Seeded {len(PLACES_ENTRIES)} places.")

    def create_bucket_list_db(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Bucket List 👽"),
            icon={"type": "emoji", "emoji": "✅"},
            is_inline=True,
            properties={
                "Item": {"title": {}},
                "Priority": {
                    "select": {
                        "options": [
                            select_option("High", "red"),
                            select_option("Medium", "yellow"),
                            select_option("Low", "gray"),
                        ]
                    }
                },
                "Category": {
                    "multi_select": {
                        "options": [
                            select_option("Travel", "blue"),
                            select_option("Adventure", "orange"),
                            select_option("Chill", "green"),
                            select_option("Fitness", "red"),
                            select_option("Creative", "purple"),
                            select_option("Social", "pink"),
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            select_option("Not Started", "gray"),
                            select_option("In Progress", "yellow"),
                            select_option("Done", "green"),
                        ]
                    }
                },
                "People": {
                    "multi_select": {
                        "options": [
                            select_option("Solo", "gray"),
                            select_option("You + BF", "pink"),
                            select_option("Friends", "purple"),
                            select_option("Family", "green"),
                        ]
                    }
                },
            },
        )
        return db["id"]

    def seed_bucket_list(self, db_id: str) -> None:
        for item, priority, cats, status, people in BUCKET_LIST_ENTRIES:
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Item": {"title": rich_text(item)},
                    "Priority": {"select": {"name": priority}},
                    "Category": {"multi_select": [{"name": c} for c in cats]},
                    "Status": {"select": {"name": status}},
                    "People": {"multi_select": [{"name": p} for p in people]},
                },
            )
        print(f"  ✓ Seeded {len(BUCKET_LIST_ENTRIES)} bucket list items.")

    def create_budget_db(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Budget Tracker 🫧"),
            icon={"type": "emoji", "emoji": "💰"},
            is_inline=True,
            properties={
                "Item": {"title": {}},
                "Category": {
                    "select": {
                        "options": [
                            select_option("Travel", "blue"),
                            select_option("Gear", "orange"),
                            select_option("Tickets", "purple"),
                            select_option("Food", "green"),
                            select_option("Other", "gray"),
                        ]
                    }
                },
                "Planned Amount": {"number": {"format": "dollar"}},
                "Actual": {"number": {"format": "dollar"}},
                "Remaining": {
                    "formula": {"expression": 'prop("Planned Amount") - prop("Actual")'}
                },
                "Trip / Outing": {
                    "select": {
                        "options": [
                            select_option("San Diego Day Trip", "blue"),
                            select_option("Beach Weekend", "yellow"),
                            select_option("Staycation Week", "green"),
                            select_option("General", "gray"),
                        ]
                    }
                },
                "Cost Level": {
                    "select": {
                        "options": [
                            select_option("Free", "green"),
                            select_option("$", "yellow"),
                            select_option("$$", "orange"),
                            select_option("$$$", "red"),
                        ]
                    }
                },
            },
        )
        return db["id"]

    def seed_budget(self, db_id: str) -> None:
        for item, cat, planned, actual, trip, cost_level in BUDGET_ENTRIES:
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Item": {"title": rich_text(item)},
                    "Category": {"select": {"name": cat}},
                    "Planned Amount": {"number": planned},
                    "Actual": {"number": actual},
                    "Trip / Outing": {"select": {"name": trip}},
                    "Cost Level": {"select": {"name": cost_level}},
                },
            )
        print(f"  ✓ Seeded {len(BUDGET_ENTRIES)} budget entries.")

    def create_highlights_db(self, page_id: str) -> str:
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=rich_text("Summer Highlights 🐶"),
            icon={"type": "emoji", "emoji": "⭐"},
            is_inline=True,
            properties={
                "Title": {"title": {}},
                "Date": {"date": {}},
                "People": {
                    "multi_select": {
                        "options": [
                            select_option("Solo", "gray"),
                            select_option("You + BF", "pink"),
                            select_option("Friends", "purple"),
                            select_option("Family", "green"),
                        ]
                    }
                },
                "Location": {"rich_text": {}},
                "Rating": {"number": {"format": "number"}},
                "Notes": {"rich_text": {}},
            },
        )
        return db["id"]

    def seed_highlights(self, db_id: str) -> None:
        for title, date, people, loc, rating, notes in HIGHLIGHTS_ENTRIES:
            self.notion.pages.create(
                parent={"type": "database_id", "database_id": db_id},
                properties={
                    "Title": {"title": rich_text(title)},
                    "Date": {"date": {"start": date}},
                    "People": {"multi_select": [{"name": p} for p in people]},
                    "Location": {"rich_text": rich_text(loc)},
                    "Rating": {"number": rating},
                    "Notes": {"rich_text": rich_text(notes)},
                },
            )
        print(f"  ✓ Seeded {len(HIGHLIGHTS_ENTRIES)} highlight entries.")

    def create_linked_view(self, page_id: str, database_id: str) -> None:
        # linked_to_database insertion is not consistently supported by the public API.
        # Add a plain URL reference to avoid noisy validation errors.
        notion_url = f"https://www.notion.so/{database_id.replace('-', '')}"
        self.notion.blocks.children.append(
            block_id=page_id,
            children=[paragraph_block(f"Open database: {notion_url}")],
        )

    def add_relations(
        self,
        master_cal_id: str,
        activities_id: str,
        bucket_list_id: str,
        highlights_id: str,
        budget_id: str,
        places_id: str,
    ) -> None:
        relation_targets = [
            ("Activities.Date", activities_id, "Date", master_cal_id),
            ("Bucket List.Linked Event", bucket_list_id, "Linked Event", master_cal_id),
            ("Summer Highlights.Activity", highlights_id, "Activity", activities_id),
            ("Budget Tracker.Associated Place", budget_id, "Associated Place", places_id),
        ]
        for label, source_db_id, prop_name, target_db_id in relation_targets:
            try:
                self.notion.databases.update(
                    database_id=source_db_id,
                    properties={
                        prop_name: {
                            "relation": {
                                "database_id": target_db_id,
                                "type": "dual_property",
                                "dual_property": {},
                            }
                        }
                    },
                )
                print(f"  ✓ {label} relation added")
            except APIResponseError as exc:
                print(f"  ⚠ {label} relation failed: {format_api_error(exc)}")

    def build_dashboard(self, page_id: str, db_ids: dict[str, str]) -> None:
        top_blocks = [
            heading_block(1, "Summer 2026 Dashboard 🦆"),
            callout_block(
                "This is for planning the BEST Summer EVER 😎"
            ),
            heading_block(2, "Summer 2026 Goals 🔥"),
            bulleted_block("Number of weekend outings (target: 10+)."),
            bulleted_block("Number of new places visited (target: 5+)."),
            bulleted_block("Number of intentional rest days (target: 1 per week)."),
            divider_block(),
            heading_block(2, "Setup Checklist 🫧"),
            todo_block("Review sample entries and customize dates 🕓"),
            todo_block("Adjust view filters to June-August 2026 4️⃣"),
            todo_block("Share page and set permissions 🦮"),
            todo_block("Add new activities and bucket list items 👽"),
            todo_block("Review budget and cost levels 🔥"),
            divider_block(),
        ]
        append_blocks(self.notion, page_id, top_blocks)

        section_map = [
            ("Planning & Schedule 🕓", "Master Calendar 🕓", db_ids.get("master_calendar", "")),
            ("Planning & Schedule 🕓", "Availability 4️⃣", db_ids.get("availability", "")),
            ("Activities & Bucket List 🔥", "Activities 🔥", db_ids.get("activities", "")),
            ("Activities & Bucket List 🔥", "Bucket List 👽", db_ids.get("bucket_list", "")),
            ("Places & Ideas 🦮", "Places to Go 🦮", db_ids.get("places", "")),
            ("Summer Highlights 🐶", "Summer Highlights 🐶", db_ids.get("highlights", "")),
            ("Budget Overview 🫧", "Budget Tracker 🫧", db_ids.get("budget", "")),
        ]

        last_section = ""
        for section, label, database_id in section_map:
            if not database_id:
                continue
            blocks = []
            if section != last_section:
                blocks.extend([divider_block(), heading_block(2, section), divider_block()])
                last_section = section
            blocks.append(paragraph_block(f"{label} database"))
            append_blocks(self.notion, page_id, blocks)
            self.create_linked_view(page_id, database_id)
        append_blocks(self.notion, page_id, [divider_block()])

    def run(self) -> int:
        print("=" * 60)
        print("Notion Summer 2026 Planner - Setup")
        print("=" * 60)

        try:
            self.settings.validate()
        except ValueError as exc:
            print(f"\n❌  {exc}")
            return 1

        try:
            main_page_id = self.create_main_page()
        except APIResponseError as exc:
            print(f"Fatal: could not create main page - {format_api_error(exc)}")
            print(
                "Tip: verify PARENT_PAGE_ID and confirm that page is shared with "
                "your Notion integration."
            )
            return 1

        db_ids: dict[str, str | None] = {}
        creation_steps: list[tuple[str, Any]] = [
            ("master_calendar", self.create_master_calendar),
            ("activities", self.create_activities_db),
            ("availability", self.create_availability_db),
            ("places", self.create_places_db),
            ("bucket_list", self.create_bucket_list_db),
            ("budget", self.create_budget_db),
            ("highlights", self.create_highlights_db),
        ]
        for key, fn in creation_steps:
            try:
                db_ids[key] = fn(main_page_id)
                print(f"  ✓ {key.replace('_', ' ').title()} created")
                time.sleep(0.4)
            except APIResponseError as exc:
                print(f"  ⚠  {key} creation failed: {format_api_error(exc)}")
                db_ids[key] = None

        print("\nSeeding sample data ...")
        seed_steps = [
            ("master_calendar", self.seed_master_calendar),
            ("activities", self.seed_activities),
            ("availability", self.seed_availability),
            ("places", self.seed_places),
            ("bucket_list", self.seed_bucket_list),
            ("budget", self.seed_budget),
            ("highlights", self.seed_highlights),
        ]
        for key, fn in seed_steps:
            db_id = db_ids.get(key)
            if not db_id:
                continue
            try:
                fn(db_id)
            except APIResponseError as exc:
                print(f"  ⚠  {key} seed failed: {exc.code}")

        required_for_relations = [
            "master_calendar",
            "activities",
            "bucket_list",
            "highlights",
            "budget",
            "places",
        ]
        if all(db_ids.get(name) for name in required_for_relations):
            self.add_relations(
                master_cal_id=db_ids["master_calendar"] or "",
                activities_id=db_ids["activities"] or "",
                bucket_list_id=db_ids["bucket_list"] or "",
                highlights_id=db_ids["highlights"] or "",
                budget_id=db_ids["budget"] or "",
                places_id=db_ids["places"] or "",
            )
        else:
            print("  ⚠  Skipping relations - one or more databases failed to create.")

        try:
            self.build_dashboard(main_page_id, {k: v or "" for k, v in db_ids.items()})
        except APIResponseError as exc:
            print(f"  ⚠  Dashboard build error: {format_api_error(exc)}")

        print("\n" + "=" * 60)
        print("Summer 2026 Planner created successfully! YAY!")
        print("=" * 60)
        print(f"\nMain page ID: {main_page_id}")
        for key, val in db_ids.items():
            print(f"  {key.replace('_', ' ').title():<22}: {val}")
        return 0


def run_from_env() -> None:
    settings = Settings.from_env()
    builder = SummerPlannerBuilder(settings)
    raise SystemExit(builder.run())

