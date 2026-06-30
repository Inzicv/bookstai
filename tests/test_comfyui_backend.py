"""Tests for the ComfyUI image backend."""

from __future__ import annotations

from pathlib import Path

import pytest

from bookstai.core.errors import EmptyPromptError, ImageGenerationError
from bookstai.image.comfyui_backend import ComfyUIHTTPClient, ComfyUIImageBackend


class FakeHTTPClient:
    def __init__(self, response: dict[str, str]) -> None:
        self.response = response
        self.last_url = None
        self.last_payload = None
        self.last_timeout = None

    def post_json(self, url: str, payload: dict[str, object], timeout: float) -> dict[str, str]:
        self.last_url = url
        self.last_payload = payload
        self.last_timeout = timeout
        return self.response


def test_comfyui_backend_can_be_imported() -> None:
    assert ComfyUIImageBackend is not None


def test_comfyui_backend_accepts_default_parameters(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(output_dir=tmp_path / "images")

    assert backend.comfyui_url == "http://127.0.0.1:8188"
    assert backend.workflow_path is None
    assert backend.output_dir == tmp_path / "images"
    assert backend.output_dir.exists()
    assert backend.timeout == 60.0
    assert backend.poll_interval == 1.0


def test_comfyui_backend_converts_workflow_and_output_paths(tmp_path: Path) -> None:
    workflow_path = tmp_path / "workflow.json"
    workflow_path.write_text("{}", encoding="utf-8")

    backend = ComfyUIImageBackend(
        workflow_path=str(workflow_path),
        output_dir=str(tmp_path / "outputs"),
    )

    assert backend.workflow_path == workflow_path
    assert isinstance(backend.output_dir, Path)
    assert backend.output_dir == tmp_path / "outputs"


def test_generate_rejects_empty_prompt(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(output_dir=tmp_path / "images", http_client=FakeHTTPClient({}))

    with pytest.raises(EmptyPromptError):
        backend.generate("")


def test_generate_calls_http_client_and_returns_image_path(tmp_path: Path) -> None:
    fake_client = FakeHTTPClient({"image_path": "outputs/images/generated.png"})
    backend = ComfyUIImageBackend(
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    result = backend.generate("a cinematic book cover")

    assert result == "outputs/images/generated.png"
    assert fake_client.last_url == "http://127.0.0.1:8188/prompt"
    assert fake_client.last_payload == {"prompt": "a cinematic book cover"}
    assert fake_client.last_timeout == 60.0


def test_generate_includes_workflow_path_in_payload(tmp_path: Path) -> None:
    workflow_path = tmp_path / "workflow.json"
    workflow_path.write_text("{}", encoding="utf-8")
    fake_client = FakeHTTPClient({"image_path": "outputs/images/generated.png"})
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    backend.generate("prompt")

    assert fake_client.last_payload == {
        "prompt": "prompt",
        "workflow_path": str(workflow_path),
    }


def test_generate_raises_when_response_lacks_image_path(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(
        output_dir=tmp_path / "images",
        http_client=FakeHTTPClient({}),
    )

    with pytest.raises(ImageGenerationError):
        backend.generate("prompt")


def test_backend_uses_comfyui_http_client_by_default(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(output_dir=tmp_path / "images")

    assert isinstance(backend.http_client, ComfyUIHTTPClient)
