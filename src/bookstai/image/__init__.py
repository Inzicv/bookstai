"""Image generation abstractions for BookstAI."""

from .backend import ImageBackend
from .comfyui_backend import ComfyUIHTTPClient, ComfyUIImageBackend
from .factory import create_image_backend
from .mock_backend import MockImageBackend
from .types import (
    ImageBackendHealthResult,
    ImageGenerationParams,
    ImageGenerationRequest,
    ImageGenerationResult,
)

__all__ = [
    "ImageBackend",
    "MockImageBackend",
    "ComfyUIImageBackend",
    "ComfyUIHTTPClient",
    "create_image_backend",
    "ImageGenerationParams",
    "ImageGenerationRequest",
    "ImageGenerationResult",
    "ImageBackendHealthResult",
]
