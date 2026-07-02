"""Shared API helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...core.errors import HITLSessionStorageError
from ...hitl import HITLSession, HITLSessionStorage


def build_memory_root() -> Path:
    return Path("memory")


def build_prompt_root() -> Path:
    return Path("prompts")


def build_output_root() -> Path:
    return Path("outputs")


def api_error(code: str, message: str) -> dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message}}


def serialize_path(path: Path | str | None) -> str | None:
    if path is None:
        return None
    return Path(path).as_posix()


def hitl_storage() -> HITLSessionStorage:
    return HITLSessionStorage(root=build_output_root() / "hitl")


def get_hitl_path(workflow_type: str, book_slug: str) -> Path:
    return build_output_root() / "hitl" / workflow_type / f"{book_slug}.json"


def save_hitl_session(session_data: dict[str, Any], workflow_type: str, book_slug: str) -> Path:
    session = HITLSession.from_dict(session_data)
    return hitl_storage().save_to_path(session, get_hitl_path(workflow_type, book_slug))


def save_loaded_hitl_session(session: HITLSession) -> Path:
    return save_hitl_session(session.to_dict(), session.workflow_name, session.item_slug)


def load_hitl_session(workflow_type: str, book_slug: str, as_session: bool = False) -> dict[str, Any]:
    path = get_hitl_path(workflow_type, book_slug)
    if not path.exists():
        return api_error("SESSION_NOT_FOUND", f"No HITL session found for {workflow_type}/{book_slug}")
    try:
        session = hitl_storage().load(path)
    except HITLSessionStorageError as exc:
        return api_error("SESSION_NOT_FOUND", str(exc))
    if as_session:
        return {"ok": True, "session": session, "path": serialize_path(path)}
    return {"ok": True, "session": session.to_dict(), "path": serialize_path(path)}
