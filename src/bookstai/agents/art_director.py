"""Art director agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class ArtDirectorAgent:
    """Generate textual art direction from validated content."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        book_context: dict[str, Any],
        style_context: dict[str, Any],
        validated_content: str,
    ) -> dict[str, str]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/art_director.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
                "validated_content": validated_content,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "art_director",
            "prompt_path": "agents/art_director.md",
            "response": response,
        }
