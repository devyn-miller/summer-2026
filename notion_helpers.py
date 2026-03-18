"""Reusable Notion payload helper functions."""

from __future__ import annotations

import time
from typing import Any


def rich_text(content: str) -> list[dict[str, Any]]:
    return [{"type": "text", "text": {"content": content}}]


def select_option(name: str, color: str = "default") -> dict[str, str]:
    return {"name": name, "color": color}


def heading_block(level: int, text: str) -> dict[str, Any]:
    tag = f"heading_{level}"
    return {"object": "block", "type": tag, tag: {"rich_text": rich_text(text)}}


def divider_block() -> dict[str, Any]:
    return {"object": "block", "type": "divider", "divider": {}}


def paragraph_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text(text)},
    }


def callout_block(text: str, emoji: str = "🏖️") -> dict[str, Any]:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": rich_text(text),
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def todo_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {"rich_text": rich_text(text), "checked": False},
    }


def bulleted_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text(text)},
    }


def db_view_block(view_type: str, db_property: str = "") -> dict[str, Any]:
    """Return a Notion database view payload for databases.create()."""
    normalized = view_type.lower()
    if normalized == "table":
        return {"type": "table", "name": "Table"}
    if normalized == "calendar":
        return {"type": "calendar", "name": "Calendar", "calendar": {"date": db_property}}
    if normalized == "timeline":
        return {"type": "timeline", "name": "Timeline", "timeline": {"date": db_property}}
    if normalized == "board":
        return {"type": "board", "name": "Board", "board": {"group_by": db_property}}
    if normalized == "gallery":
        return {"type": "gallery", "name": "Gallery"}
    raise ValueError(f"Unsupported database view type: {view_type}")


def column_list_block(
    col_a_blocks: list[dict[str, Any]],
    col_b_blocks: list[dict[str, Any]],
) -> dict[str, Any]:
    # Notion expects nested children under column_list and each column payload.
    return {
        "object": "block",
        "type": "column_list",
        "column_list": {
            "children": [
                {
                    "object": "block",
                    "type": "column",
                    "column": {"children": col_a_blocks},
                },
                {
                    "object": "block",
                    "type": "column",
                    "column": {"children": col_b_blocks},
                },
            ]
        },
    }


def append_blocks(notion: Any, page_id: str, blocks: list[dict[str, Any]]) -> None:
    """Append blocks in batches of 100 (API limit)."""
    for i in range(0, len(blocks), 100):
        notion.blocks.children.append(block_id=page_id, children=blocks[i : i + 100])
        time.sleep(0.3)

