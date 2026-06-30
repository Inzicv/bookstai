"""Review writer agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class ReviewWriterAgent:
    """Generate a first humoristic review draft from structured inputs."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        book_context: dict[str, Any],
        style_context: dict[str, Any],
        comedy_bank: dict[str, Any],
        user_opinion: str,
    ) -> dict[str, str]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/review_writer.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
                "comedy_bank": comedy_bank,
                "user_opinion": user_opinion,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "review_writer",
            "prompt_path": "agents/review_writer.md",
            "response": response,
        }
