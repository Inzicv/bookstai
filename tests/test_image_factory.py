"""Tests for the image backend factory."""

from __future__ import annotations

from pathlib import Path

import pytest

from bookstai.core.errors import UnsupportedImageBackendError
from bookstai.image import ComfyUIImageBackend, MockImageBackend, create_image_backend


def test_create_image_backend_can_be_imported() -> None:
    assert create_image_backend is not None


def test_create_image_backend_returns_mock_backend() -> None:
    backend = create_image_backend(backend="mock")

    assert isinstance(backend, MockImageBackend)
    assert backend.image_path == "outputs/mock/image.png"


def test_create_image_backend_returns_mock_backend_with_custom_image_path() -> None:
    backend = create_image_backend(backend="mock", image_path="outputs/mock/custom.png")

    assert isinstance(backend, MockImageBackend)
    assert backend.image_path == "outputs/mock/custom.png"


def test_create_image_backend_returns_comfyui_backend(monkeypatch, tmp_path: Path) -> None:
    captured = {}

    class DummyComfyUIImageBackend:
        def __init__(
            self,
            comfyui_url: str,
            workflow_path: str | Path | None,
            output_dir: str | Path,
            timeout: float,
            poll_interval: float,
        ) -> None:
            captured["comfyui_url"] = comfyui_url
            captured["workflow_path"] = workflow_path
            captured["output_dir"] = output_dir
            captured["timeout"] = timeout
            captured["poll_interval"] = poll_interval

    monkeypatch.setattr("bookstai.image.factory.ComfyUIImageBackend", DummyComfyUIImageBackend)

    backend = create_image_backend(
        backend="comfyui",
        comfyui_url="http://127.0.0.1:8188",
        workflow_path="workflows/comfyui/book_cover.json",
        output_dir=tmp_path / "images",
        timeout=60.0,
        poll_interval=1.0,
    )

    assert isinstance(backend, DummyComfyUIImageBackend)
    assert captured["comfyui_url"] == "http://127.0.0.1:8188"
    assert captured["workflow_path"] == "workflows/comfyui/book_cover.json"
    assert captured["output_dir"] == tmp_path / "images"
    assert captured["timeout"] == 60.0
    assert captured["poll_interval"] == 1.0


def test_create_image_backend_rejects_unknown_backend() -> None:
    with pytest.raises(UnsupportedImageBackendError) as exc_info:
        create_image_backend(backend="whatever")  # type: ignore[arg-type]

    assert "whatever" in str(exc_info.value)
