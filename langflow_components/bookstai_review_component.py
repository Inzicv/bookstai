"""Langflow custom component for the BookstAI Review workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bookstai.langflow.review_component import run_review_workflow

try:
    from langflow.custom import Component
    from langflow.io import MessageTextInput, Output
    from langflow.schema import Data
except ImportError as exc:  # pragma: no cover - only affects local Langflow runtime
    raise ImportError(
        "Langflow is required to use BookstAIReviewComponent."
    ) from exc


class BookstAIReviewComponent(Component):
    display_name = "BookstAI Review"
    name = "BookstAIReviewComponent"
    description = "Run the BookstAI Review workflow with local mocks."
    icon = "book-open"

    inputs = [
        MessageTextInput(
            name="book_slug",
            display_name="Book slug",
            info="Slug of the book memory file to load.",
        ),
        MessageTextInput(
            name="user_opinion",
            display_name="User opinion",
            info="User opinion passed to the Review workflow.",
        ),
        MessageTextInput(
            name="platform",
            display_name="Platform",
            value="tiktok",
            info="Target social platform.",
        ),
        MessageTextInput(
            name="memory_root",
            display_name="Memory root",
            value="memory",
            info="Root folder for BookstAI memory files.",
        ),
        MessageTextInput(
            name="prompt_root",
            display_name="Prompt root",
            value="prompts",
            info="Root folder for BookstAI prompt files.",
        ),
    ]

    outputs = [
        Output(
            display_name="Result",
            name="result",
            method="build",
            output_type=Data,
        )
    ]

    def build(self) -> Data:
        result = run_review_workflow(
            book_slug=self.book_slug,
            user_opinion=self.user_opinion,
            platform=self.platform,
            memory_root=Path(self.memory_root),
            prompt_root=Path(self.prompt_root),
        )
        return Data(value=result)
