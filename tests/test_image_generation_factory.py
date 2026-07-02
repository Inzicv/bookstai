from __future__ import annotations

import os
from pathlib import Path

import pytest

from bookstai.core.errors import UnsupportedImageBackendError
from bookstai.image_generation import MockImageBackend, OpenAIImageBackend, create_image_backend


def test_create_image_backend_returns_mock_backend() -> None:
    backend = create_image_backend("mock")
    assert isinstance(backend, MockImageBackend)


def test_create_image_backend_returns_openai_backend() -> None:
    backend = create_image_backend("openai", model="gpt-image-2", quality="high")
    assert isinstance(backend, OpenAIImageBackend)


def test_create_image_backend_rejects_comfyui_not_ready() -> None:
    with pytest.raises(UnsupportedImageBackendError):
        create_image_backend("comfyui")

