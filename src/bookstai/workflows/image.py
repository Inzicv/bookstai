"""Image workflow orchestrator for BookstAI."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from ..agents.art_director import ArtDirectorAgent
from ..agents.context_builder import ContextBuilder
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

    def generate_storyboard(
        self,
        book_slug: str,
        lyrics: str,
        visual_style_id: str,
        format: str = "4:5",
        brief: str | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        book_context = self.context_builder.build(book_slug=book_slug, workflow_type="visual", spoiler_level="full")
        visual_style = self.visual_style_reader.read_style(visual_style_id)
        item_slug = self._build_item_slug(book_slug, visual_style_id, lyrics, format)
        style_context = {
            "visual_style": visual_style,
            "brief": brief or "",
            "format": format,
        }
        storyboard_result = self.art_director_agent.generate(
            book_context=book_context,
            style_context=style_context,
            validated_song=lyrics,
        )
        scenes = storyboard_result.get("scenes", [])
        session = HITLSession(workflow_name="visual", item_slug=item_slug)
        for scene in scenes:
            session.add_step(name=f"storyboard_{scene['scene_id']}", content=scene)
        return {
            "workflow": "visual",
            "stage": "storyboard",
            "book_slug": book_slug,
            "item_slug": item_slug,
            "visual_style_id": visual_style["id"],
            "visual_style": visual_style,
            "book_context": book_context,
            "lyrics": lyrics,
            "format": format,
            "brief": brief or "",
            "storyboard": {"scenes": scenes},
            "hitl": session.to_dict(),
            "legacy": legacy_kwargs or {},
        }

    def generate_character_prompts(
        self,
        item_slug: str,
        book_slug: str,
        visual_style_id: str,
        storyboard: dict[str, Any],
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        validated_scenes = storyboard.get("scenes", [])
        if not validated_scenes or not all(scene.get("status") in {"approved", "edited"} for scene in validated_scenes):
            raise ValueError("Storyboard scenes must be approved before generating character prompts.")
        book_context = self.context_builder.build(book_slug=book_slug, workflow_type="visual", spoiler_level="full")
        visual_style = self.visual_style_reader.read_style(visual_style_id)
        prompt_result = self.prompt_maker_agent.generate(
            validated_storyboard=storyboard,
            style_context={"visual_style": visual_style},
            book_context=book_context,
            prompt_kind="characters",
        )
        session = HITLSession(workflow_name="visual", item_slug=item_slug)
        for prompt in prompt_result.get("prompts", []):
            session.add_step(name=prompt["prompt_id"], content=prompt)
        return {
            "workflow": "visual",
            "stage": "character_prompts",
            "book_slug": book_slug,
            "item_slug": item_slug,
            "visual_style_id": visual_style_id,
            "character_prompts": prompt_result.get("prompts", []),
            "hitl": session.to_dict(),
            "legacy": legacy_kwargs or {},
        }

    def generate_background_prompts(
        self,
        item_slug: str,
        book_slug: str,
        visual_style_id: str,
        storyboard: dict[str, Any],
        character_prompts: list[dict[str, Any]] | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        validated_character_prompts = character_prompts or []
        if not validated_character_prompts or not all(prompt.get("status") in {"approved", "edited"} for prompt in validated_character_prompts):
            raise ValueError("Character prompts must be approved before generating backgrounds.")
        book_context = self.context_builder.build(book_slug=book_slug, workflow_type="visual", spoiler_level="full")
        visual_style = self.visual_style_reader.read_style(visual_style_id)
        prompt_result = self.prompt_maker_agent.generate(
            validated_storyboard=storyboard,
            style_context={"visual_style": visual_style},
            book_context=book_context,
            prompt_kind="backgrounds",
        )
        session = HITLSession(workflow_name="visual", item_slug=item_slug)
        for prompt in prompt_result.get("prompts", []):
            session.add_step(name=prompt["prompt_id"], content=prompt)
        return {
            "workflow": "visual",
            "stage": "background_prompts",
            "book_slug": book_slug,
            "item_slug": item_slug,
            "visual_style_id": visual_style_id,
            "background_prompts": prompt_result.get("prompts", []),
            "hitl": session.to_dict(),
            "legacy": legacy_kwargs or {},
        }

    def generate_batch(
        self,
        item_slug: str,
        storyboard: dict[str, Any],
        character_prompts: list[dict[str, Any]],
        background_prompts: list[dict[str, Any]],
        backend: str = "mock",
        confirm_generation: bool = False,
        **_: Any,
    ) -> dict[str, Any]:
        if not confirm_generation:
            return {
                "workflow": "visual",
                "stage": "batch",
                "item_slug": item_slug,
                "backend": backend,
                "images": [],
                "error": {
                    "code": "GENERATION_NOT_CONFIRMED",
                    "message": "Generation must be confirmed before batch generation.",
                },
            }
        if not all(prompt.get("status") == "approved" for prompt in character_prompts + background_prompts):
            return {
                "workflow": "visual",
                "stage": "batch",
                "item_slug": item_slug,
                "backend": backend,
                "images": [],
                "error": {
                    "code": "PROMPTS_NOT_FULLY_APPROVED",
                    "message": "All prompts must be approved before batch generation.",
                },
            }
        if backend != "mock":
            return {
                "workflow": "visual",
                "stage": "batch",
                "item_slug": item_slug,
                "backend": backend,
                "images": [],
                "error": {
                    "code": "IMAGE_GENERATION_BACKEND_NOT_READY",
                    "message": "Image generation backend is not ready yet.",
                },
            }
        images = [
            {
                "image_id": f"image_{scene['scene_id']}",
                "scene_id": scene["scene_id"],
                "prompt_id": character_prompts[0]["prompt_id"] if character_prompts else "character_prompt",
                "backend": "mock",
                "status": "generated",
                "output_path": f"outputs/visual/{item_slug}/{scene['scene_id']}.png",
                "preview_url": f"/preview/{item_slug}/{scene['scene_id']}",
                "generation_parameters": {},
                "review_comment": None,
                "created_at": "2026-07-02T00:00:00Z",
            }
            for scene in storyboard.get("scenes", [])
        ]
        return {
            "workflow": "visual",
            "stage": "batch",
            "item_slug": item_slug,
            "backend": backend,
            "images": images,
            "error": None,
        }

    def run(
        self,
        book_slug: str,
        lyrics: str,
        visual_style_id: str,
        format: str = "4:5",
        brief: str | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        storyboard = self.generate_storyboard(book_slug, lyrics, visual_style_id, format=format, brief=brief)
        character_prompts = self.generate_character_prompts(
            item_slug=storyboard["item_slug"],
            book_slug=book_slug,
            visual_style_id=visual_style_id,
            storyboard=storyboard["storyboard"],
        )
        background_prompts = self.generate_background_prompts(
            item_slug=storyboard["item_slug"],
            book_slug=book_slug,
            visual_style_id=visual_style_id,
            storyboard=storyboard["storyboard"],
            character_prompts=character_prompts["character_prompts"],
        )
        return {
            **storyboard,
            "character_prompts": character_prompts["character_prompts"],
            "background_prompts": background_prompts["background_prompts"],
            "legacy": legacy_kwargs or {},
        }

    def run_with_hitl(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return self.generate_storyboard(*args, **kwargs)

    def _build_item_slug(self, book_slug: str, visual_style_id: str, lyrics: str, format: str) -> str:
        digest = hashlib.sha1(f"{book_slug}|{visual_style_id}|{format}|{lyrics}".encode("utf-8")).hexdigest()
        return f"{book_slug}-{visual_style_id}-{digest[:10]}"
