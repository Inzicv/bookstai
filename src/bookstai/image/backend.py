"""Image backend protocol."""

from __future__ import annotations

from typing import Protocol

from .types import ImageBackendHealthResult, ImageGenerationRequest, ImageGenerationResult


class ImageBackend(Protocol):
    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        ...

    def healthcheck(self) -> ImageBackendHealthResult:
        ...
