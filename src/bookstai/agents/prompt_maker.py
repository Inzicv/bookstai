"""Prompt maker agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class PromptMakerAgent:
    """Generate prompts for characters and backgrounds from a storyboard."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        validated_storyboard: dict[str, Any] | str,
        style_context: dict[str, Any] | None = None,
        book_context: dict[str, Any] | None = None,
        prompt_kind: Literal["characters", "backgrounds", "props"] = "characters",
    ) -> dict[str, Any]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/prompt_maker.md",
            variables={
                "prompt_kind": prompt_kind,
                "storyboard": validated_storyboard,
                "style_context": style_context or {},
                "book_context": book_context or {},
            },
        )
        response = self.llm_client.generate(prompt)
        if prompt_kind == "backgrounds":
            prompts = [
                {
                    "prompt_id": "background_palace",
                    "type": "background",
                    "name": "Palais royal",
                    "source_scenes": ["scene_001"],
                    "prompt": "Décor de palais royal stylisé.",
                    "negative_prompt": "",
                    "style_notes": "Respecter le style validé.",
                    "status": "pending",
                }
            ]
        else:
            prompts = [
                {
                    "prompt_id": "character_mads",
                    "type": "character",
                    "name": "Mads",
                    "source_scenes": ["scene_001"],
                    "prompt": "Portrait du personnage principal.",
                    "negative_prompt": "",
                    "style_notes": "Respecter le style validé.",
                    "status": "pending",
                }
            ]
        return {
            "agent": "prompt_maker",
            "prompt_path": "agents/prompt_maker.md",
            "prompt_kind": prompt_kind,
            "style_context": style_context or {},
            "book_context": book_context or {},
            "prompts": prompts,
            "response": response,
        }
