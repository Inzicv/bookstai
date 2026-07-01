"""Learning API schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class LearningExtractRequest(BaseModel):
    type: Literal["review", "song"]
    book_slug: str


class LearningDraftRequest(LearningExtractRequest):
    pass


class LearningApplyRequest(BaseModel):
    draft_path: str
    confirm: bool = False
    memory_file: str | None = None

