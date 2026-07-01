"""Song routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ...core.errors import UnsupportedImageBackendError, UnsupportedProviderError
from ...image import create_image_backend
from ...llm import create_llm_client
from ...workflows.song import SongWorkflow
from ..schemas.song import SongRunRequest
from .shared import api_error, build_memory_root, build_prompt_root, save_hitl_session, serialize_path

router = APIRouter(prefix="/song", tags=["song"])


@router.post("/run")
def run_song(payload: SongRunRequest) -> dict[str, Any]:
    if payload.provider != "mock":
        return api_error("INVALID_PROVIDER", "Only the mock provider is allowed in local API mode.")
    if payload.image_backend != "mock":
        return api_error("INVALID_PROVIDER", "Only the mock image backend is allowed in local API mode.")

    try:
        workflow = SongWorkflow(
            memory_root=build_memory_root(),
            prompt_root=build_prompt_root(),
            llm_client=create_llm_client(provider=payload.provider, model=payload.model or "gpt-4o-mini", temperature=payload.temperature),
            image_backend=create_image_backend(backend=payload.image_backend, image_path="outputs/mock/image.png"),
        )
        result = (
            workflow.run_with_hitl(
                book_slug=payload.book_slug,
                spoiler_mode=payload.spoiler_mode,
                prompt_type=payload.prompt_type,
                platform=payload.platform,
            )
            if payload.hitl_enabled
            else workflow.run(
                book_slug=payload.book_slug,
                spoiler_mode=payload.spoiler_mode,
                prompt_type=payload.prompt_type,
                platform=payload.platform,
            )
        )
        hitl_path = None
        if payload.hitl_enabled and "hitl" in result:
            hitl_path = serialize_path(save_hitl_session(result["hitl"], "song", payload.book_slug))
        return {
            "ok": True,
            "type": "song",
            "book_slug": payload.book_slug,
            "provider": payload.provider,
            "image_backend": payload.image_backend,
            "hitl_enabled": payload.hitl_enabled,
            "result": result,
            "hitl_session_path": hitl_path,
        }
    except (UnsupportedProviderError, UnsupportedImageBackendError) as exc:
        return api_error("INVALID_PROVIDER", str(exc))
    except Exception as exc:  # pragma: no cover - defensive boundary
        return api_error("WORKFLOW_ERROR", str(exc))
