"""Prompt maker agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class PromptMakerAgent:
    """Generate character and background prompts from a storyboard."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        validated_storyboard: dict[str, Any] | str,
        style_context: dict[str, Any] | None = None,
        book_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/prompt_maker.md",
            variables={
                "storyboard": validated_storyboard,
                "style_context": style_context or {},
                "book_context": book_context or {},
            },
        )
        response = self.llm_client.generate(prompt)
        return {
            "agent": "prompt_maker",
            "prompt_path": "agents/prompt_maker.md",
            "style_context": style_context or {},
            "book_context": book_context or {},
            "character_prompts": [
                {"name": "Personnage principal", "prompt": "Portrait du personnage principal"}
            ],
            "background_prompts": [
                {"name": "Décor principal", "prompt": "Décor principal du livre"}
            ],
            "prop_prompts": [],
            "style_notes": "Prompts compatibles storyboard.",
            "response": response,
        }
