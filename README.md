# AWESOME Summer 2026 Notion Planner

This awesome repo is to design a complete Notion planning workspace for Summer 2026!! Yay I'm so excited tehehe

It includes:

1. Main page: `Summer 2026 Planner`
2. Databases:
   - Master Calendar
   - Activities
   - Availability
   - Places to Go
   - Bucket List
   - Budget Tracker
   - Summer Highlights
3. Sample entries for each database
4. Relations between relevant databases
5. Dashboard sections with linked database blocks (or fallbacks)

But like we can always add more manually or via this repo!

## Project Structure

```text
summer-2026/
├── notion_main.py        # Script entrypoint
├── cli.py                # Thin CLI wrapper
├── builder.py            # Core orchestration + Notion API operations
├── config.py             # .env loading + validation
├── notion_helpers.py     # Shared payload/block helper functions
├── sample_data.py        # Seed datasets
├── .env
├── requirements.txt
└── README.md
```

## Requirements

- Python
- Notion integration token
- Notion parent page ID where the planner should be created

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python notion_main.py
```

## Customization

- Edit sample records in `sample_data.py`
- Adjust database schema/properties in `builder.py`
- Modify dashboard text/sections in `SummerPlannerBuilder.build_dashboard`
