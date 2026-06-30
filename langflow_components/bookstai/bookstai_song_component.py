"""Langflow custom component for the BookstAI Song workflow."""

from __future__ import annotations

from pathlib import Path

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data

from bookstai.langflow.song_component import run_song_workflow


class BookstAISongComponent(Component):
    display_name = "BookstAI Song"
    name = "BookstAISongComponent"
    description = "Run the BookstAI Song workflow with local mocks."
    icon = "music"

    inputs = [
        MessageTextInput(
            name="book_slug",
            display_name="Book slug",
            info="Slug of the book memory file to load.",
        ),
        MessageTextInput(
            name="spoiler_mode",
            display_name="Spoiler mode",
            value="spoiler_free",
            info="Spoiler mode passed to the Song workflow.",
        ),
        MessageTextInput(
            name="prompt_type",
            display_name="Prompt type",
            value="thumbnail",
            info="Prompt type passed to the Song workflow.",
        ),
        MessageTextInput(
            name="platform",
            display_name="Platform",
            value="tiktok",
            info="Target social platform.",
        ),
        MessageTextInput(
            name="provider",
            display_name="Provider",
            value="mock",
            info="LLM provider used by the adapter.",
        ),
        MessageTextInput(
            name="model",
            display_name="Model",
            value="gpt-4o-mini",
            info="Model name passed to the LLM factory.",
        ),
        MessageTextInput(
            name="temperature",
            display_name="Temperature",
            value="0.7",
            info="Sampling temperature passed to the LLM factory.",
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
        MessageTextInput(
            name="image_path",
            display_name="Image path",
            value="outputs/mock/image.png",
            info="Mock image output path.",
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
        result = run_song_workflow(
            book_slug=self.book_slug,
            spoiler_mode=self.spoiler_mode,
            prompt_type=self.prompt_type,
            platform=self.platform,
            memory_root=Path(self.memory_root),
            prompt_root=Path(self.prompt_root),
            image_path=Path(self.image_path),
            provider=self.provider,
            model=self.model,
            temperature=float(self.temperature),
        )
        return Data(value=result)
