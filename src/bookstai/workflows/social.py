"""Social workflow orchestrator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..agents.context_builder import ContextBuilder
from ..agents.social_media import SocialMediaAgent
from ..agents.style_memory import StyleMemoryAgent
from ..llm.client import LLMClient


class SocialWorkflow:
    def __init__(self, memory_root: Path, prompt_root: Path, llm_client: LLMClient) -> None:
        self.context_builder = ContextBuilder(memory_root=memory_root)
        self.style_memory_agent = StyleMemoryAgent(memory_root=memory_root)
        self.social_media_agent = SocialMediaAgent(prompt_root=prompt_root, llm_client=llm_client)

    def run(
        self,
        book_slug: str,
        source_type: str = "review",
        source_content: str | None = None,
    ) -> dict[str, Any]:
        context = self.context_builder.build(book_slug=book_slug, workflow_type="social", spoiler_level="none")
        style = self.style_memory_agent.build()
        validated_content = source_content or ""
        result = self.social_media_agent.generate(validated_content=validated_content, style_context=style, platform="instagram")
        instagram = result["response"] + "\n\n#bookstagramfr"
        tiktok = result["response"] + "\n\n#booktokfr"
        return {"workflow": "social", "book_slug": book_slug, "context": context, "style": style, "instagram_caption": instagram, "tiktok_caption": tiktok}
