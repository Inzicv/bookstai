"""Song routes."""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter

from ...core.errors import MissingAPIKeyError, UnsupportedProviderError
from ...llm import create_llm_client
from ...workflows.song import SongWorkflow
from ..schemas.song import SongRunRequest
from .shared import api_error, build_memory_root, build_prompt_root, save_hitl_session, serialize_path

router = APIRouter(prefix="/song", tags=["song"])


@router.post("/run")
def run_song(payload: SongRunRequest) -> dict[str, Any]:
    if payload.provider not in {"mock", "openai"}:
        return api_error("INVALID_PROVIDER", "Provider must be one of: mock, openai.")

    try:
        if payload.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            return api_error(
                "MISSING_API_KEY",
                "OPENAI_API_KEY is required to use the openai provider.",
            )
        workflow = SongWorkflow(
            memory_root=build_memory_root(),
            prompt_root=build_prompt_root(),
            llm_client=create_llm_client(
                provider=payload.provider,
                model=payload.model or "gpt-4o-mini",
                temperature=payload.temperature,
            ),
        )
        result = (
            workflow.run_with_hitl(
                book_slug=payload.book_slug,
                story_scope=payload.story_scope,
                song_style=payload.song_style,
                platform=payload.platform,
            )
            if payload.hitl_enabled
            else workflow.run(
                book_slug=payload.book_slug,
                story_scope=payload.story_scope,
                song_style=payload.song_style,
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
            "story_scope": payload.story_scope,
            "song_style": payload.song_style,
            "platform": payload.platform,
            "provider": payload.provider,
            "model": payload.model,
            "temperature": payload.temperature,
            "hitl_enabled": payload.hitl_enabled,
            "result": result,
            "hitl_session_path": hitl_path,
        }
    except MissingAPIKeyError:
        return api_error("MISSING_API_KEY", "OPENAI_API_KEY is required to use the openai provider.")
    except ImportError:
        return api_error("OPENAI_DEPENDENCY_MISSING", "The openai package is required to use the openai provider.")
    except UnsupportedProviderError as exc:
        return api_error("INVALID_PROVIDER", str(exc))
    except Exception as exc:  # pragma: no cover - defensive boundary
        return api_error("WORKFLOW_ERROR", str(exc))
