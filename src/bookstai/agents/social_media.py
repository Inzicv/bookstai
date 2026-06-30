"""Social media agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.errors import InvalidPlatformError
from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder

SUPPORTED_PLATFORMS = {"instagram", "tiktok", "youtube_shorts"}


class SocialMediaAgent:
    """Generate social media content from validated content and style context."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        validated_content: str,
        style_context: dict[str, Any],
        platform: str,
    ) -> dict[str, str]:
        if platform not in SUPPORTED_PLATFORMS:
            raise InvalidPlatformError("Invalid social media platform.")

        prompt = self.prompt_builder.build(
            prompt_path="agents/social_media.md",
            variables={
                "validated_content": validated_content,
                "style_context": style_context,
                "platform": platform,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "social_media",
            "prompt_path": "agents/social_media.md",
            "platform": platform,
            "response": response,
        }
