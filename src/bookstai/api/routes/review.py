"""Review routes."""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter

from ...core.errors import MissingAPIKeyError, UnsupportedProviderError
from ...llm import create_llm_client
from ...workflows.pitch import PitchWorkflow
from ..schemas.review import ReviewRunRequest
from .shared import api_error, build_memory_root, build_prompt_root, save_hitl_session, serialize_path

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/run")
def run_review(payload: ReviewRunRequest) -> dict[str, Any]:
    if payload.provider not in {"mock", "openai"}:
        return api_error("INVALID_PROVIDER", "Provider must be one of: mock, openai.")

    try:
        if payload.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            return api_error(
                "MISSING_API_KEY",
                "OPENAI_API_KEY is required to use the openai provider.",
            )
        workflow = PitchWorkflow(
            memory_root=build_memory_root(),
            prompt_root=build_prompt_root(),
            llm_client=create_llm_client(provider=payload.provider, model=payload.model or "gpt-4o-mini"),
        )
        item_slug = payload.item_slug or payload.book_slug
        summary = payload.summary or payload.user_opinion
        if not item_slug:
            return api_error("INVALID_REQUEST", "item_slug or book_slug is required.")
        if not summary:
            return api_error("INVALID_REQUEST", "summary or user_opinion is required.")
        result = workflow.run_with_hitl(item_slug, summary) if payload.hitl_enabled else workflow.run(item_slug, summary)
        hitl_path = None
        if payload.hitl_enabled and "hitl" in result:
            hitl_path = serialize_path(save_hitl_session(result["hitl"], "pitch", item_slug))
        return {
            "ok": True,
            "type": "pitch",
            "item_slug": item_slug,
            "provider": payload.provider,
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
