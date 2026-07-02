"""Image routes."""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter

from ...core.errors import MissingAPIKeyError, UnsupportedProviderError
from ...exports import ExportService
from ...llm import create_llm_client
from ...workflows.image import ImageWorkflow
from ..schemas.image import ImageRunRequest
from .shared import (
    api_error,
    build_memory_root,
    build_output_root,
    build_prompt_root,
    save_hitl_session,
    serialize_path,
)

router = APIRouter(prefix="/image", tags=["image"])


@router.get("/styles")
def list_styles() -> dict[str, Any]:
    workflow = _build_workflow(provider="mock", model=None, temperature=0.0)
    return {"ok": True, "styles": workflow.list_styles()}


@router.post("/run")
def run_image(payload: ImageRunRequest) -> dict[str, Any]:
    if payload.provider not in {"mock", "openai"}:
        return api_error("INVALID_PROVIDER", "Provider must be one of: mock, openai.")

    try:
        if payload.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            return api_error(
                "MISSING_API_KEY",
                "OPENAI_API_KEY is required to use the openai provider.",
            )
        workflow = _build_workflow(
            provider=payload.provider,
            model=payload.model,
            temperature=payload.temperature,
        )
        result = (
            workflow.run_with_hitl(
                lyrics=payload.lyrics,
                visual_style_id=payload.visual_style_id,
                platform=payload.platform,
                format=payload.format,
                brief=payload.brief,
            )
            if payload.hitl_enabled
            else workflow.run(
                lyrics=payload.lyrics,
                visual_style_id=payload.visual_style_id,
                platform=payload.platform,
                format=payload.format,
                brief=payload.brief,
            )
        )
        hitl_path = None
        if payload.hitl_enabled and "hitl" in result:
            hitl_path = serialize_path(
                save_hitl_session(result["hitl"], "visual", payload.visual_style_id)
            )
        export_paths: dict[str, str] | None = None
        if payload.export_formats:
            export_paths = {
                key: str(value)
                for key, value in ExportService(output_root=build_output_root()).export(
                    workflow_name="visual",
                    item_slug=payload.visual_style_id,
                    data=result,
                    formats=payload.export_formats,
                ).items()
            }
        return {
            "ok": True,
            "type": "visual",
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


def _build_workflow(provider: str, model: str | None, temperature: float) -> ImageWorkflow:
    return ImageWorkflow(
        memory_root=build_memory_root(),
        prompt_root=build_prompt_root(),
        llm_client=create_llm_client(provider=provider, model=model or "gpt-4o-mini", temperature=temperature),
    )
