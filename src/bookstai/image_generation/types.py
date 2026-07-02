"""Types for image generation backends."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ImageBackendName = Literal["mock", "openai", "comfyui"]
ImageQuality = Literal["low", "medium", "high"]


@dataclass(slots=True)
class GeneratedImageArtifact:
    image_id: str
    scene_id: str
    prompt_id: str | None
    backend: str
    status: Literal["generated", "approved", "revision_requested", "failed"]
    output_path: str
    preview_url: str | None = None
    generation_parameters: dict[str, Any] = field(default_factory=dict)
    review_comment: str | None = None
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ImageGenerationCostEstimate:
    currency: str
    estimated_min: float
    estimated_max: float
    assumptions: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ImageGenerationRequest:
    item_slug: str
    backend: ImageBackendName = "mock"
    model: str | None = None
    quality: ImageQuality | None = "medium"
    storyboard: dict[str, Any] = field(default_factory=dict)
    character_prompts: list[dict[str, Any]] = field(default_factory=list)
    background_prompts: list[dict[str, Any]] = field(default_factory=list)
    format: str = "4:5"
    width: int | None = None
    height: int | None = None
    steps: int = 25
    cfg: float = 7.0
    seed: int | None = None
    confirm_generation: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ImageGenerationResult:
    ok: bool
    backend: str
    model: str | None
    quality: ImageQuality | None
    estimated_cost: ImageGenerationCostEstimate | None
    images: list[GeneratedImageArtifact] = field(default_factory=list)
    error_code: str | None = None
    error_message: str | None = None
    generation_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "backend": self.backend,
            "model": self.model,
            "quality": self.quality,
            "estimated_cost": None if self.estimated_cost is None else self.estimated_cost.to_dict(),
            "images": [image.to_dict() for image in self.images],
            "error_code": self.error_code,
            "error_message": self.error_message,
            "generation_path": self.generation_path,
        }
