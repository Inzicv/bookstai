"""Review API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class ReviewRunRequest(BaseModel):
    item_slug: str | None = None
    book_slug: str | None = None
    summary: str | None = None
    user_opinion: str | None = None
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None
    hitl_enabled: bool = True


class ReviewRunResponse(BaseModel):
    ok: bool
    type: Literal["pitch"]
    item_slug: str
    provider: Literal["mock", "openai"]
    hitl_enabled: bool
    result: dict[str, Any]
    hitl_session_path: str | None = None
