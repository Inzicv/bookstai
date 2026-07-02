"""Factory helpers for image generation backends."""

from __future__ import annotations

from pathlib import Path

from ..core.errors import UnsupportedImageBackendError
from .backend import ImageBackend
from .mock_backend import MockImageBackend
from .openai_backend import OpenAIImageBackend
from .types import ImageBackendName


def create_image_backend(
    backend: ImageBackendName,
    model: str | None = None,
    quality: str | None = None,
    output_root: str | Path = "outputs/images",
) -> ImageBackend:
    if backend == "mock":
        return MockImageBackend(output_root=output_root, model=model, quality=quality)
    if backend == "openai":
        return OpenAIImageBackend(output_root=output_root, model=model, quality=quality)
    if backend == "comfyui":
        raise UnsupportedImageBackendError("IMAGE_BACKEND_NOT_READY")
    raise UnsupportedImageBackendError("UNSUPPORTED_IMAGE_BACKEND")
