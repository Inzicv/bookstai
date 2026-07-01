"""HITL routes."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter

from ...core.errors import HITLStepNotFoundError
from ..schemas.hitl import HITLActionRequest, HITLEditRequest
from .shared import api_error, load_hitl_session, save_loaded_hitl_session, serialize_path

router = APIRouter(prefix="/hitl", tags=["hitl"])


@router.get("/session")
def get_session(type: Literal["review", "song"], book_slug: str) -> dict[str, Any]:
    return load_hitl_session(type, book_slug)


@router.post("/approve")
def approve(payload: HITLActionRequest) -> dict[str, Any]:
    return _apply_action(payload.type, payload.book_slug, payload.step_id, "approve", payload.comment)


@router.post("/reject")
def reject(payload: HITLActionRequest) -> dict[str, Any]:
    return _apply_action(payload.type, payload.book_slug, payload.step_id, "reject", payload.comment)


@router.post("/edit")
def edit(payload: HITLEditRequest) -> dict[str, Any]:
    return _apply_action(
        payload.type,
        payload.book_slug,
        payload.step_id,
        "edit",
        payload.comment,
        payload.edited_content,
    )


def _apply_action(
    workflow_type: str,
    book_slug: str,
    step_id: str,
    action: str,
    comment: str | None = None,
    edited_content: Any | None = None,
) -> dict[str, Any]:
    session = load_hitl_session(workflow_type, book_slug, as_session=True)
    if "error" in session:
        return session
    hitl_session = session["session"]
    try:
        if action == "approve":
            hitl_session.approve_step(step_id, comment=comment)
        elif action == "reject":
            hitl_session.reject_step(step_id, comment=comment)
        elif action == "edit":
            hitl_session.edit_step(step_id, edited_content=edited_content, comment=comment)
        else:
            return api_error("WORKFLOW_ERROR", f"Unknown HITL action: {action}")
        path = save_loaded_hitl_session(hitl_session)
        return {"ok": True, "session": hitl_session.to_dict(), "path": serialize_path(path)}
    except HITLStepNotFoundError as exc:
        return api_error("STEP_NOT_FOUND", str(exc))
    except Exception as exc:
        return api_error("STEP_NOT_FOUND", str(exc))
