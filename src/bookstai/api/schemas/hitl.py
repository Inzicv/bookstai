"""HITL API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class HITLActionRequest(BaseModel):
    type: Literal["review", "song", "visual"]
    book_slug: str
    step_id: str
    comment: str | None = None


class HITLEditRequest(HITLActionRequest):
    edited_content: Any


class HITLSessionResponse(BaseModel):
    ok: bool
    session: Any
    path: str
