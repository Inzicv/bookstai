"""Comedy room agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class ComedyRoomAgent:
    """Generate a humor idea bank from book and style contexts."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        book_context: dict[str, Any],
        style_context: dict[str, Any],
    ) -> dict[str, str]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/comedy_room.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "comedy_room",
            "prompt_path": "agents/comedy_room.md",
            "response": response,
        }
