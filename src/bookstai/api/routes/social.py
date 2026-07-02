"""Social routes."""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter

from ...core.errors import MissingAPIKeyError, UnsupportedProviderError
from ...llm import create_llm_client
from ...workflows.social import SocialWorkflow
from ..schemas.social import SocialRunRequest
from .shared import api_error, build_memory_root, build_prompt_root

router = APIRouter(prefix="/social", tags=["social"])


@router.post("/run")
def run_social(payload: SocialRunRequest) -> dict[str, Any]:
    if payload.provider not in {"mock", "openai"}:
        return api_error("INVALID_PROVIDER", "Provider must be one of: mock, openai.")
    try:
        if payload.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            return api_error("MISSING_API_KEY", "OPENAI_API_KEY is required to use the openai provider.")
        workflow = SocialWorkflow(
            memory_root=build_memory_root(),
            prompt_root=build_prompt_root(),
            llm_client=create_llm_client(provider=payload.provider, model=payload.model or "gpt-4o-mini"),
        )
        result = workflow.run(payload.book_slug, payload.source_type, payload.source_content)
        return {"ok": True, "type": "social", "book_slug": payload.book_slug, "provider": payload.provider, "result": result}
    except MissingAPIKeyError:
        return api_error("MISSING_API_KEY", "OPENAI_API_KEY is required to use the openai provider.")
    except ImportError:
        return api_error("OPENAI_DEPENDENCY_MISSING", "The openai package is required to use the openai provider.")
    except UnsupportedProviderError as exc:
        return api_error("INVALID_PROVIDER", str(exc))
    except Exception as exc:
        return api_error("WORKFLOW_ERROR", str(exc))
