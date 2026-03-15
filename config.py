"""Configuration loading and validation."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    notion_token: str
    parent_page_id: str
    cover_image_url: str = (
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1500"
    )

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            notion_token=os.getenv(
                "NOTION_TOKEN",
                "integration_token",
            ),
            parent_page_id=os.getenv(
                "PARENT_PAGE_ID",
                "parent_page_id",
            ),
            cover_image_url=os.getenv(
                "COVER_IMAGE_URL",
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1500",
            ),
        )

    def validate(self) -> None:
        if self.notion_token == "integration_token":
            raise ValueError("Missing NOTION_TOKEN :(")
        if self.parent_page_id == "parent_page_id":
            raise ValueError("Missing PARENT_PAGE_ID :(")

