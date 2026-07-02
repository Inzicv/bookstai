"""Image API schemas."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ImageStyleItem(BaseModel):
    id: str
    name: str
    source_path: str
    instructions: str
    sections: dict[str, str] = Field(default_factory=dict)


class ImageStylesResponse(BaseModel):
    ok: bool
    styles: list[ImageStyleItem]


class ImageRunRequest(BaseModel):
    lyrics: str
    visual_style_id: str
    platform: Literal["instagram", "tiktok", "youtube_shorts"] = "instagram"
    format: str = "4:5"
    brief: str | None = None
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None
    temperature: float = 0.7
    hitl_enabled: bool = True
    export_formats: list[Literal["markdown", "json"]] = Field(default_factory=list)


class ImageRunResponse(BaseModel):
    ok: bool
    type: Literal["visual"]
    item_slug: str
    visual_style_id: str
    provider: Literal["mock", "openai"]
    model: str | None = None
    temperature: float
    hitl_enabled: bool
    result: dict[str, Any]
    hitl_session_path: str | None = None
    export_paths: dict[str, str] | None = None
