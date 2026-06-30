"""Prompt maker agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.errors import InvalidPromptTypeError
from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder

SUPPORTED_PROMPT_TYPES = {"character", "scene", "thumbnail", "video"}


class PromptMakerAgent:
    """Transform validated art direction into image-oriented prompts."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(self, art_direction: str, prompt_type: str) -> dict[str, str]:
        if prompt_type not in SUPPORTED_PROMPT_TYPES:
            raise InvalidPromptTypeError("Invalid image prompt type.")

        prompt = self.prompt_builder.build(
            prompt_path="agents/prompt_maker.md",
            variables={
                "art_direction": art_direction,
                "prompt_type": prompt_type,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "prompt_maker",
            "prompt_path": "agents/prompt_maker.md",
            "prompt_type": prompt_type,
            "response": response,
        }
