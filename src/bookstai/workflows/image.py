"""Image workflow orchestrator for BookstAI."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from ..agents.context_builder import ContextBuilder
from ..agents.art_director import ArtDirectorAgent
from ..agents.prompt_maker import PromptMakerAgent
from ..hitl import HITLSession
from ..llm.client import LLMClient
from ..visual import VisualStyleReader


class ImageWorkflow:
    """Orchestrate the image workflow from lyrics and a selected visual style."""

    def __init__(self, memory_root: Path, prompt_root: Path, llm_client: LLMClient, **_: Any) -> None:
        self.context_builder = ContextBuilder(memory_root=memory_root)
        self.visual_style_reader = VisualStyleReader(memory_root=memory_root)
        self.art_director_agent = ArtDirectorAgent(prompt_root=prompt_root, llm_client=llm_client)
        self.prompt_maker_agent = PromptMakerAgent(prompt_root=prompt_root, llm_client=llm_client)

    def list_styles(self) -> list[dict[str, Any]]:
        return self.visual_style_reader.list_styles()

    def run(
        self,
        book_slug: str,
        lyrics: str,
        visual_style_id: str,
        platform: str = "instagram",
        format: str = "4:5",
        brief: str | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        return self._run_steps(
            book_slug=book_slug,
            lyrics=lyrics,
            visual_style_id=visual_style_id,
            platform=platform,
            format=format,
            brief=brief,
            legacy_kwargs=legacy_kwargs,
        )

    def run_with_hitl(
        self,
        book_slug: str,
        lyrics: str,
        visual_style_id: str,
        platform: str = "instagram",
        format: str = "4:5",
        brief: str | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        result = self._run_steps(
            book_slug=book_slug,
            lyrics=lyrics,
            visual_style_id=visual_style_id,
            platform=platform,
            format=format,
            brief=brief,
            legacy_kwargs=legacy_kwargs,
        )
        session = HITLSession(workflow_name="visual", item_slug=result["item_slug"])
        session.add_step(name="style_selection", content=result["style_selection"])
        session.add_step(name="storyboard", content=result["storyboard"])
        session.add_step(name="prompts", content=result["prompts"])
        result["hitl"] = session.to_dict()
        return result

    def _run_steps(
        self,
        book_slug: str,
        lyrics: str,
        visual_style_id: str,
        platform: str,
        format: str,
        brief: str | None,
        legacy_kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        book_context = self.context_builder.build(
            book_slug=book_slug,
            workflow_type="visual",
            spoiler_level="full",
        )
        visual_style = self.visual_style_reader.read_style(visual_style_id)
        item_slug = self._build_item_slug(book_slug, visual_style_id, lyrics, platform, format)
        style_context = {
            "visual_style": visual_style,
            "brief": brief or "",
            "platform": platform,
            "format": format,
        }
        image_context = {
            "workflow": "visual",
            "book_slug": book_slug,
            "book_context": book_context,
            "lyrics": lyrics,
            "item_slug": item_slug,
            "brief": brief or "",
            "platform": platform,
            "format": format,
            "visual_style_id": visual_style_id,
        }
        style_selection = {
            "book_slug": book_slug,
            "visual_style_id": visual_style["id"],
            "visual_style": visual_style,
            "brief": brief or "",
            "platform": platform,
            "format": format,
        }
        storyboard = self.art_director_agent.generate(
            book_context=book_context,
            style_context=style_context,
            validated_song=lyrics,
        )
        prompts = self.prompt_maker_agent.generate(
            validated_storyboard=storyboard,
            style_context=style_context,
            book_context=book_context,
        )
        return {
            "workflow": "visual",
            "book_slug": book_slug,
            "book_context": book_context,
            "lyrics": lyrics,
            "item_slug": item_slug,
            "visual_style_id": visual_style["id"],
            "visual_style": visual_style,
            "style_selection": style_selection,
            "image_context": image_context,
            "storyboard": storyboard,
            "prompts": prompts,
            "brief": brief or "",
            "platform": platform,
            "format": format,
            "legacy": legacy_kwargs or {},
        }

    def _build_item_slug(self, book_slug: str, visual_style_id: str, lyrics: str, platform: str, format: str) -> str:
        digest = hashlib.sha1(f"{book_slug}|{visual_style_id}|{platform}|{format}|{lyrics}".encode("utf-8")).hexdigest()
        return f"{book_slug}-{visual_style_id}-{digest[:10]}"
