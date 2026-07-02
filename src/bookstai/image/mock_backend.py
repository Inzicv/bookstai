"""Mock image backend for BookstAI."""

from __future__ import annotations

from .backend import ImageBackend
from .types import ImageBackendHealthResult, ImageGenerationRequest, ImageGenerationResult


class MockImageBackend:
    def __init__(self, image_path: str = "outputs/mock/image.png") -> None:
        self.image_path = image_path
        self.last_prompt: str | None = None
        self.last_request: ImageGenerationRequest | None = None

    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        self.last_request = request
        self.last_prompt = request.prompt
        return ImageGenerationResult(
            ok=True,
            backend="mock",
            image_path=self.image_path,
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            params=request.params.to_dict(),
        )

    def healthcheck(self) -> ImageBackendHealthResult:
        return ImageBackendHealthResult(
            ok=True,
            backend="mock",
            message="Mock image backend is available.",
        )
