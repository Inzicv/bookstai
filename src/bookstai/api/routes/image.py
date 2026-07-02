"""Image routes."""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter

from ...core.errors import MissingAPIKeyError, UnsupportedProviderError
from ...exports import ExportService
from ...llm import create_llm_client
from ...workflows.image import ImageWorkflow
from ..schemas.image import (
    ImageBackgroundPromptsRequest,
    ImageBatchGenerationRequest,
    ImageCharacterPromptsRequest,
    ImageRunRequest,
    ImageStoryboardApprovalRequest,
    ImageStoryboardApprovalResponse,
    ImageStoryboardRequest,
)
from .shared import (
    api_error,
    build_memory_root,
    build_output_root,
    build_prompt_root,
    load_hitl_session,
    save_hitl_session,
    serialize_path,
)

router = APIRouter(prefix="/image", tags=["image"])


@router.get("/styles")
def list_styles() -> dict[str, Any]:
    workflow = _build_workflow(provider="mock", model=None, temperature=0.0)
    return {"ok": True, "styles": workflow.list_styles()}


@router.post("/storyboard")
def storyboard(payload: ImageStoryboardRequest) -> dict[str, Any]:
    result = _run_storyboard(payload)
    if result.get("hitl"):
        _merge_and_save_hitl_session("visual", result["item_slug"], result["hitl"])
    return result


@router.post("/storyboard/approve")
def approve_storyboard(payload: ImageStoryboardApprovalRequest) -> dict[str, Any]:
    scenes = payload.storyboard.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        return api_error("STORYBOARD_EMPTY", "Storyboard must contain at least one scene.")
    for scene in scenes:
        if not isinstance(scene, dict) or scene.get("status") not in {"approved", "edited"}:
            return api_error(
                "STORYBOARD_NOT_FULLY_APPROVED",
                "All storyboard scenes must be approved or edited before continuing.",
            )
    storyboard_path = build_output_root() / "visual" / payload.item_slug / "storyboard-approved.json"
    storyboard_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        storyboard_path.write_text(
            __import__("json").dumps(
                {
                    "type": "image_storyboard_approval",
                    "item_slug": payload.item_slug,
                    "book_slug": payload.book_slug,
                    "visual_style_id": payload.visual_style_id,
                    "storyboard": payload.storyboard,
                    "approved": True,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    except OSError:
        return api_error("STORYBOARD_SAVE_FAILED", "Could not save approved storyboard.")
    return {
        "ok": True,
        "type": "image_storyboard_approval",
        "item_slug": payload.item_slug,
        "book_slug": payload.book_slug,
        "visual_style_id": payload.visual_style_id,
        "storyboard_path": storyboard_path.as_posix(),
        "storyboard": payload.storyboard,
    }


@router.post("/prompts/characters")
def character_prompts(payload: ImageCharacterPromptsRequest) -> dict[str, Any]:
    workflow = _build_workflow(provider=payload.provider, model=payload.model, temperature=payload.temperature)
    result = workflow.generate_character_prompts(
        item_slug=payload.item_slug,
        book_slug=payload.book_slug,
        visual_style_id=payload.visual_style_id,
        storyboard=payload.storyboard,
    )
    if result.get("hitl"):
        _merge_and_save_hitl_session("visual", payload.item_slug, result["hitl"])
    return {"ok": True, **result}


@router.post("/prompts/backgrounds")
def background_prompts(payload: ImageBackgroundPromptsRequest) -> dict[str, Any]:
    workflow = _build_workflow(provider=payload.provider, model=payload.model, temperature=payload.temperature)
    result = workflow.generate_background_prompts(
        item_slug=payload.item_slug,
        book_slug=payload.book_slug,
        visual_style_id=payload.visual_style_id,
        storyboard=payload.storyboard,
        character_prompts=payload.character_prompts,
    )
    if result.get("hitl"):
        _merge_and_save_hitl_session("visual", payload.item_slug, result["hitl"])
    return {"ok": True, **result}


@router.post("/generate-batch")
def generate_batch(payload: ImageBatchGenerationRequest) -> dict[str, Any]:
    workflow = _build_workflow(provider="mock", model=None, temperature=0.0)
    result = workflow.generate_batch(
        item_slug=payload.item_slug,
        storyboard=payload.storyboard,
        character_prompts=payload.character_prompts,
        background_prompts=payload.background_prompts,
        backend=payload.backend,
        confirm_generation=payload.confirm_generation,
    )
    return {"ok": result.get("error") is None, **result}


@router.post("/run")
def run_image(payload: ImageRunRequest) -> dict[str, Any]:
    if payload.provider not in {"mock", "openai"}:
        return api_error("INVALID_PROVIDER", "Provider must be one of: mock, openai.")
    try:
        if payload.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            return api_error("MISSING_API_KEY", "OPENAI_API_KEY is required to use the openai provider.")
        workflow = _build_workflow(provider=payload.provider, model=payload.model, temperature=payload.temperature)
        result = workflow.run(
            book_slug=payload.book_slug,
            lyrics=payload.lyrics,
            visual_style_id=payload.visual_style_id,
            format=payload.format,
            brief=payload.brief,
        )
        hitl_path = None
        if payload.hitl_enabled and "hitl" in result:
            hitl_path = serialize_path(save_hitl_session(result["hitl"], "visual", result["item_slug"]))
        export_paths: dict[str, str] | None = None
        if payload.export_formats:
            export_paths = {
                key: str(value)
                for key, value in ExportService(output_root=build_output_root()).export(
                    workflow_name="visual",
                    item_slug=result["item_slug"],
                    data=result,
                    formats=payload.export_formats,
                ).items()
            }
        return {
            "ok": True,
            "type": "visual",
            "book_slug": payload.book_slug,
            "item_slug": result["item_slug"],
            "visual_style_id": payload.visual_style_id,
            "provider": payload.provider,
            "model": payload.model,
            "temperature": payload.temperature,
            "hitl_enabled": payload.hitl_enabled,
            "result": result,
            "hitl_session_path": hitl_path,
            "export_paths": export_paths,
        }
    except MissingAPIKeyError:
        return api_error("MISSING_API_KEY", "OPENAI_API_KEY is required to use the openai provider.")
    except ImportError:
        return api_error("OPENAI_DEPENDENCY_MISSING", "The openai package is required to use the openai provider.")
    except UnsupportedProviderError as exc:
        return api_error("INVALID_PROVIDER", str(exc))
    except FileNotFoundError as exc:
        return api_error("STYLE_NOT_FOUND", str(exc))
    except Exception as exc:  # pragma: no cover - defensive boundary
        return api_error("WORKFLOW_ERROR", str(exc))


def _run_storyboard(payload: ImageStoryboardRequest) -> dict[str, Any]:
    workflow = _build_workflow(provider=payload.provider, model=payload.model, temperature=payload.temperature)
    result = workflow.generate_storyboard(
        book_slug=payload.book_slug,
        lyrics=payload.lyrics,
        visual_style_id=payload.visual_style_id,
        format=payload.format,
        brief=payload.brief,
    )
    return {"ok": True, **result}


def _merge_and_save_hitl_session(workflow_type: str, item_slug: str, session_data: dict[str, Any]) -> None:
    existing = load_hitl_session(workflow_type, item_slug, as_session=True)
    if "session" in existing:
        session = existing["session"]
        for step_data in session_data.get("steps", []):
            session.add_step(
                name=step_data["name"],
                content=step_data["content"],
                metadata=step_data.get("metadata") or {},
            )
            if step_data.get("status") == "approved":
                session.approve_step(step_data["name"], comment=step_data.get("comment"))
            elif step_data.get("status") == "rejected":
                session.reject_step(step_data["name"], comment=step_data.get("comment"))
            elif step_data.get("status") == "edited":
                session.edit_step(
                    step_data["name"],
                    edited_content=step_data.get("edited_content"),
                    comment=step_data.get("comment"),
                )
        save_hitl_session(session.to_dict(), workflow_type, item_slug)
        return
    save_hitl_session(session_data, workflow_type, item_slug)


def _build_workflow(provider: str, model: str | None, temperature: float) -> ImageWorkflow:
    return ImageWorkflow(
        memory_root=build_memory_root(),
        prompt_root=build_prompt_root(),
        llm_client=create_llm_client(provider=provider, model=model or "gpt-4o-mini", temperature=temperature),
    )
