"""Song API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class SongRunRequest(BaseModel):
    book_slug: str
    spoiler_mode: str
    prompt_type: str
    platform: str
    provider: Literal["mock"] = "mock"
    image_backend: Literal["mock"] = "mock"
    model: str | None = None
    temperature: float = 0.7
    hitl_enabled: bool = True


class SongRunResponse(BaseModel):
    ok: bool
    type: Literal["song"]
    book_slug: str
    provider: Literal["mock"]
    image_backend: Literal["mock"]
    hitl_enabled: bool
    result: dict[str, Any]
    hitl_session_path: str | None = None

