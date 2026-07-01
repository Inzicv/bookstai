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

    def generate(self, art_direction: dict[str, Any]) -> dict[str, Any]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/prompt_maker.md",
            variables={
                "art_direction": art_direction,
            },
        )
        response = self.llm_client.generate(prompt)
        return {
            "agent": "prompt_maker",
            "prompt_path": "agents/prompt_maker.md",
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
