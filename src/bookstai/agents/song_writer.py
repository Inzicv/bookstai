"""Song writer agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.errors import InvalidSpoilerModeError
from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder

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
        story_scope: str = "pitch_only",
        song_style: str = "parody",
        spoiler_mode: str | None = None,
    ) -> dict[str, Any]:
        effective_story_scope = story_scope
        if spoiler_mode is not None:
            effective_story_scope = "pitch_only" if spoiler_mode == "spoiler_free" else "full_spoilers"
        if effective_story_scope not in {"pitch_only", "full_spoilers"}:
            raise InvalidSpoilerModeError("Invalid song story scope.")

        prompt = self.prompt_builder.build(
            prompt_path="agents/song_writer.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
                "comedy_bank": comedy_bank,
                "story_scope": effective_story_scope,
                "song_style": song_style,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "song_writer",
            "prompt_path": "agents/song_writer.md",
            "title": "BookstAI Song",
            "concept": "Parodie musicale du livre",
            "story_scope": effective_story_scope,
            "spoiler_mode": "spoiler_free" if effective_story_scope == "pitch_only" else "full",
            "song_style": song_style,
            "lyrics": response,
            "structure_notes": "Couplet-refrain adaptables pour validation humaine.",
            "response": response,
        }
