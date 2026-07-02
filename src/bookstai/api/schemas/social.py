"""Social API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class SocialRunRequest(BaseModel):
    book_slug: str
    source_type: Literal["review", "song", "free_text"] = "review"
    source_content: str | None = None
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None


class SocialRunResponse(BaseModel):
    ok: bool
    type: Literal["social"]
    book_slug: str
    provider: Literal["mock", "openai"]
    result: dict[str, Any]
