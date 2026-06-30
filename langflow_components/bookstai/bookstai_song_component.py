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
        MessageTextInput(
            name="image_backend",
            display_name="Image backend",
            value="mock",
            info="Image backend used by the Song workflow.",
        ),
        MessageTextInput(
            name="comfyui_url",
            display_name="ComfyUI URL",
            value="http://127.0.0.1:8188",
            info="Local ComfyUI endpoint.",
        ),
        MessageTextInput(
            name="comfyui_workflow_path",
            display_name="ComfyUI workflow path",
            value="",
            info="Path to a ComfyUI workflow file.",
        ),
        MessageTextInput(
            name="image_output_dir",
            display_name="Image output dir",
            value="outputs/images",
            info="Directory used by the image backend.",
        ),
        MessageTextInput(
            name="image_timeout",
            display_name="Image timeout",
            value="60.0",
            info="Timeout passed to the image backend factory.",
        ),
        MessageTextInput(
            name="image_poll_interval",
            display_name="Image poll interval",
            value="1.0",
            info="Polling interval passed to the image backend factory.",
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
            image_backend=self.image_backend,
            comfyui_url=self.comfyui_url,
            comfyui_workflow_path=Path(self.comfyui_workflow_path) if self.comfyui_workflow_path else None,
            image_output_dir=Path(self.image_output_dir),
            image_timeout=float(self.image_timeout),
            image_poll_interval=float(self.image_poll_interval),
        )
        return Data(value=result)
