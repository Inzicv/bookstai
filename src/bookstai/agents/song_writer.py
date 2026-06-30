"""Song writer agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.errors import InvalidSpoilerModeError
from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder

SUPPORTED_SPOILER_MODES = {"spoiler_free", "full"}


class SongWriterAgent:
    """Generate a first parody song draft from structured inputs."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        book_context: dict[str, Any],
        style_context: dict[str, Any],
        comedy_bank: dict[str, Any],
        spoiler_mode: str,
    ) -> dict[str, str]:
        if spoiler_mode not in SUPPORTED_SPOILER_MODES:
            raise InvalidSpoilerModeError("Invalid song spoiler mode.")

        prompt = self.prompt_builder.build(
            prompt_path="agents/song_writer.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
                "comedy_bank": comedy_bank,
                "spoiler_mode": spoiler_mode,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "song_writer",
            "prompt_path": "agents/song_writer.md",
            "spoiler_mode": spoiler_mode,
            "response": response,
        }
