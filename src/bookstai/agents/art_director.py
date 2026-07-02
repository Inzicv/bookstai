"""Art director agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class ArtDirectorAgent:
    """Generate a scene-by-scene storyboard from the validated song."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        book_context: dict[str, Any],
        style_context: dict[str, Any],
        validated_song: str | dict[str, Any],
    ) -> dict[str, Any]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/art_director.md",
            variables={
                "book_context": book_context,
                "style_context": style_context,
                "validated_song": validated_song,
            },
        )
        response = self.llm_client.generate(prompt)
        scenes = [
            {
                "scene_id": "scene_001",
                "scene_number": 1,
                "song_part": "Couplet 1",
                "lyrics_excerpt": "Ouverture du morceau.",
                "visual_intention": "Introduire le monde et le ton.",
                "characters": ["Personnage principal"],
                "background": "Décor principal",
                "key_props": ["Objet symbolique"],
                "camera": "Plan large",
                "movement": "Travelling lent",
                "transition": "cut",
                "style_notes": "Respecter le style validé.",
                "status": "pending",
            },
            {
                "scene_id": "scene_002",
                "scene_number": 2,
                "song_part": "Refrain",
                "lyrics_excerpt": "Montée émotionnelle.",
                "visual_intention": "Accentuer le rythme et l'énergie.",
                "characters": ["Personnage principal"],
                "background": "Lieu secondaire",
                "key_props": [],
                "camera": "Plan rapproché",
                "movement": "Panoramique",
                "transition": "cut",
                "style_notes": "Conserver la cohérence visuelle.",
                "status": "pending",
            },
        ]
        return {
            "agent": "art_director",
            "prompt_path": "agents/art_director.md",
            "scenes": scenes,
            "response": response,
        }
