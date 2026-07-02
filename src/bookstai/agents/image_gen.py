"""Image generation agent for BookstAI."""

from __future__ import annotations

from ..image.backend import ImageBackend
from ..image.types import ImageGenerationRequest, ImageGenerationResult


class ImageGenAgent:
    """Delegate image generation to an injected backend."""

    def __init__(self, backend: ImageBackend) -> None:
        self.backend = backend

    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        return self.backend.generate(request)
