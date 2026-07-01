"""Song API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class SongRunRequest(BaseModel):
    book_slug: str
    story_scope: Literal["pitch_only", "full_spoilers"] = "pitch_only"
    song_style: Literal["parody"] = "parody"
    platform: Literal["tiktok", "instagram"] = "tiktok"
    provider: Literal["mock"] = "mock"
    model: str | None = None
    temperature: float = 0.7
    hitl_enabled: bool = True


class SongRunResponse(BaseModel):
    ok: bool
    type: Literal["song"]
    book_slug: str
    story_scope: Literal["pitch_only", "full_spoilers"]
    song_style: Literal["parody"]
    platform: Literal["tiktok", "instagram"]
    provider: Literal["mock"]
    model: str | None = None
    temperature: float
    result: dict[str, Any]
    hitl_enabled: bool
    hitl_session_path: str | None = None
