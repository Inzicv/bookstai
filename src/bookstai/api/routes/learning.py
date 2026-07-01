"""Learning routes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter

from ...core.errors import LearningApplyError
from ...learning import LearningDraftApplier, LearningDraftWriter, LearningExtractor
from ..schemas.learning import LearningApplyRequest, LearningDraftRequest, LearningExtractRequest
from .shared import api_error, load_hitl_session

router = APIRouter(prefix="/learning", tags=["learning"])


@router.post("/extract")
def extract(payload: LearningExtractRequest) -> dict[str, Any]:
    loaded = load_hitl_session(payload.type, payload.book_slug, as_session=True)
    if "error" in loaded:
        return loaded
    extraction = LearningExtractor().extract(loaded["session"])
    return {"ok": True, "extraction": extraction.to_dict()}


@router.post("/draft")
def draft(payload: LearningDraftRequest) -> dict[str, Any]:
    loaded = load_hitl_session(payload.type, payload.book_slug, as_session=True)
    if "error" in loaded:
        return loaded
    extraction = LearningExtractor().extract(loaded["session"])
    path = LearningDraftWriter().write(extraction)
    return {"ok": True, "draft_path": str(path), "markdown": path.read_text(encoding="utf-8")}


@router.post("/apply")
def apply(payload: LearningApplyRequest) -> dict[str, Any]:
    if payload.confirm is not True:
        return api_error("CONFIRMATION_REQUIRED", "Learning apply requires confirm=true.")
    try:
        memory_file = payload.memory_file
        if memory_file is None:
            draft_name = Path(payload.draft_path).name.replace("-learning-draft.md", ".md")
            memory_file = f"books/{draft_name}"
        result = LearningDraftApplier().apply(payload.draft_path, memory_file)
        return {
            "ok": True,
            "draft_path": str(result.draft_path),
            "memory_path": str(result.memory_path),
            "backup_path": str(result.backup_path) if result.backup_path else None,
            "applied": result.applied,
        }
    except LearningApplyError as exc:
        return api_error("DRAFT_NOT_FOUND", str(exc))
