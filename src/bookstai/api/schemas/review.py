"""Review API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class ReviewRunRequest(BaseModel):
    book_slug: str
    user_opinion: str
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None
    hitl_enabled: bool = True


class ReviewRunResponse(BaseModel):
    ok: bool
    type: Literal["review"]
    book_slug: str
    provider: Literal["mock", "openai"]
    hitl_enabled: bool
    result: dict[str, Any]
    hitl_session_path: str | None = None
