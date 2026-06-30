"""Factory helpers for BookstAI image backends."""

from __future__ import annotations

from pathlib import Path

from ..core.errors import UnsupportedImageBackendError
from ..core.types import ImageBackendType
from .backend import ImageBackend
from .comfyui_backend import ComfyUIImageBackend
from .mock_backend import MockImageBackend


def create_image_backend(
    backend: ImageBackendType = "mock",
    image_path: str = "outputs/mock/image.png",
    comfyui_url: str = "http://127.0.0.1:8188",
    workflow_path: str | Path | None = None,
    output_dir: str | Path = "outputs/images",
    timeout: float = 60.0,
    poll_interval: float = 1.0,
) -> ImageBackend:
    if backend == "mock":
        return MockImageBackend(image_path=image_path)
    if backend == "comfyui":
        return ComfyUIImageBackend(
            comfyui_url=comfyui_url,
            workflow_path=workflow_path,
            output_dir=output_dir,
            timeout=timeout,
            poll_interval=poll_interval,
        )
    raise UnsupportedImageBackendError(
        f"Image backend '{backend}' is not supported yet."
    )
