"""Typed contracts for BookstAI image generation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ImageBackendName = Literal["mock", "comfyui"]


@dataclass(slots=True)
class ImageGenerationParams:
    width: int = 1024
    height: int = 1280
    steps: int = 25
    cfg: float = 7.0
    seed: int | None = None
    sampler: str | None = None
    model: str | None = None
    workflow_path: str | None = None
    output_dir: str = "outputs/images"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ImageGenerationRequest:
    prompt: str
    negative_prompt: str = ""
    backend: ImageBackendName = "mock"
    params: ImageGenerationParams = field(default_factory=ImageGenerationParams)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "backend": self.backend,
            "params": self.params.to_dict(),
        }


@dataclass(slots=True)
class ImageGenerationResult:
    ok: bool
    backend: str
    image_path: str | None
    prompt: str
    negative_prompt: str = ""
    params: dict[str, Any] | None = None
    error_code: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "backend": self.backend,
            "image_path": self.image_path,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "params": self.params or {},
            "error_code": self.error_code,
            "error_message": self.error_message,
        }


@dataclass(slots=True)
class ImageBackendHealthResult:
    ok: bool
    backend: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "backend": self.backend,
            "message": self.message,
        }
