"""Image generation backend protocol."""

from __future__ import annotations

from typing import Protocol

from .types import ImageGenerationRequest, ImageGenerationResult


class ImageBackend(Protocol):
    name: str
    model: str | None

    def generate_batch(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        ...
