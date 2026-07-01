"""Art director agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class ArtDirectorAgent:
    """Generate a storyboard for the validated song."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        book_context: dict[str, Any],
        style_context: dict[str, Any],
        song: dict[str, Any],
    ) -> dict[str, Any]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/art_director.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
                "validated_content": song,
            },
        )
        response = self.llm_client.generate(prompt)
        storyboard = [
            {
                "shot_number": 1,
                "lyrics_reference": "Ouverture",
                "visual_intention": "Installer l'univers du livre en version parodique.",
                "entry_image_idea": "Plan large sur le décor principal.",
                "exit_image_idea": "Le décor se transforme pour la scène suivante.",
                "characters": ["Personnage principal"],
                "background": "Décor principal",
                "movement": "Panoramique lent",
                "transition": "cut",
                "difficulty": "simple",
            }
        ]
        return {
            "agent": "art_director",
            "prompt_path": "agents/art_director.md",
            "storyboard": storyboard,
            "response": response,
        }
