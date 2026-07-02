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
    book_slug: str
    lyrics: str
    visual_style_id: str
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
    book_slug: str
    item_slug: str
    visual_style_id: str
    provider: Literal["mock", "openai"]
    model: str | None = None
    temperature: float
    hitl_enabled: bool
    result: dict[str, Any]
    hitl_session_path: str | None = None
    export_paths: dict[str, str] | None = None


class ImageStoryboardRequest(BaseModel):
    book_slug: str
    lyrics: str
    visual_style_id: str
    format: str = "4:5"
    brief: str | None = None
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None
    temperature: float = 0.7
    hitl_enabled: bool = True
    export_formats: list[Literal["markdown", "json"]] = Field(default_factory=list)


class ImageStoryboardResponse(BaseModel):
    ok: bool
    workflow: Literal["visual"]
    stage: Literal["storyboard"]
    book_slug: str
    item_slug: str
    visual_style_id: str
    visual_style: dict[str, Any]
    book_context: dict[str, Any]
    lyrics: str
    format: str
    brief: str
    storyboard: dict[str, Any]
    hitl: dict[str, Any] | None = None


class ImageStoryboardApprovalRequest(BaseModel):
    item_slug: str
    book_slug: str
    visual_style_id: str
    storyboard: dict[str, Any]


class ImageStoryboardApprovalResponse(BaseModel):
    ok: bool
    type: Literal["image_storyboard_approval"]
    item_slug: str
    book_slug: str
    visual_style_id: str
    storyboard_path: str
    storyboard: dict[str, Any]


class ImageCharacterPromptsRequest(BaseModel):
    item_slug: str
    book_slug: str
    visual_style_id: str
    storyboard: dict[str, Any]
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None
    temperature: float = 0.7
    hitl_enabled: bool = True
    export_formats: list[Literal["markdown", "json"]] = Field(default_factory=list)


class ImageCharacterPromptsResponse(BaseModel):
    ok: bool
    workflow: Literal["visual"]
    stage: Literal["character_prompts"]
    book_slug: str
    item_slug: str
    visual_style_id: str
    character_prompts: list[dict[str, Any]]
    hitl: dict[str, Any] | None = None


class ImageBackgroundPromptsRequest(BaseModel):
    item_slug: str
    book_slug: str
    visual_style_id: str
    storyboard: dict[str, Any]
    character_prompts: list[dict[str, Any]] = Field(default_factory=list)
    provider: Literal["mock", "openai"] = "mock"
    model: str | None = None
    temperature: float = 0.7
    hitl_enabled: bool = True
    export_formats: list[Literal["markdown", "json"]] = Field(default_factory=list)


class ImageBackgroundPromptsResponse(BaseModel):
    ok: bool
    workflow: Literal["visual"]
    stage: Literal["background_prompts"]
    book_slug: str
    item_slug: str
    visual_style_id: str
    background_prompts: list[dict[str, Any]]
    hitl: dict[str, Any] | None = None


class ImageBatchGenerationRequest(BaseModel):
    item_slug: str
    backend: Literal["mock", "comfyui"] = "mock"
    storyboard: dict[str, Any]
    character_prompts: list[dict[str, Any]]
    background_prompts: list[dict[str, Any]]
    width: int = 1024
    height: int = 1280
    steps: int = 25
    cfg: float = 7.0
    seed: int | None = None
    confirm_generation: bool = False


class ImageBatchGenerationResponse(BaseModel):
    ok: bool
    workflow: Literal["visual"]
    stage: Literal["batch"]
    item_slug: str
    backend: Literal["mock", "comfyui"]
    images: list[dict[str, Any]] = Field(default_factory=list)
    error: dict[str, Any] | None = None
