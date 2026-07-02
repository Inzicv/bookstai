"""Tests for the ComfyUI image backend."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from bookstai.core.errors import EmptyPromptError, ImageGenerationError
from bookstai.image.comfyui_backend import ComfyUIHTTPClient, ComfyUIImageBackend
from bookstai.image.types import ImageGenerationParams, ImageGenerationRequest


class FakeHTTPClient:
    def __init__(
        self,
        post_response: dict[str, object] | None = None,
        get_responses: list[dict[str, object]] | None = None,
        bytes_response: bytes | None = None,
    ) -> None:
        self.post_response = post_response or {}
        self.get_responses = get_responses or []
        self.bytes_response = bytes_response or b""
        self.last_post_url = None
        self.last_post_payload = None
        self.last_post_timeout = None
        self.last_get_urls: list[str] = []
        self.last_get_timeouts: list[float] = []
        self.last_bytes_url = None
        self.last_bytes_timeout = None

    def post_json(self, url: str, payload: dict[str, object], timeout: float) -> dict[str, object]:
        self.last_post_url = url
        self.last_post_payload = payload
        self.last_post_timeout = timeout
        return self.post_response

    def get_json(self, url: str, timeout: float) -> dict[str, object]:
        self.last_get_urls.append(url)
        self.last_get_timeouts.append(timeout)
        if self.get_responses:
            return self.get_responses.pop(0)
        return {}

    def get_bytes(self, url: str, timeout: float) -> bytes:
        self.last_bytes_url = url
        self.last_bytes_timeout = timeout
        return self.bytes_response


def _workflow_file(tmp_path: Path, content: str = """{"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "__BOOKSTAI_PROMPT__"}}}""") -> Path:
    workflow_path = tmp_path / "workflow.json"
    workflow_path.write_text(content, encoding="utf-8")
    return workflow_path


def _request(prompt: str, *, workflow_path: str | Path | None = None, output_dir: str | Path = "outputs/images", negative_prompt: str = "") -> ImageGenerationRequest:
    return ImageGenerationRequest(
        prompt=prompt,
        negative_prompt=negative_prompt,
        backend="comfyui",
        params=ImageGenerationParams(workflow_path=str(workflow_path) if workflow_path is not None else None, output_dir=str(output_dir)),
    )


def test_generate_rejects_empty_prompt(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(output_dir=tmp_path / "images", http_client=FakeHTTPClient())

    with pytest.raises(EmptyPromptError):
        backend.generate(_request(""))


def test_generate_uses_real_cycle_when_workflow_exists(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {"9": {"images": [{"filename": "bookstai_00001.png", "subfolder": "", "type": "output"}]}}}}],
        bytes_response=b"PNGDATA",
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    result = backend.generate(_request("a cinematic book cover"))

    assert result.ok is True
    assert result.backend == "comfyui"
    assert result.image_path == str(tmp_path / "images" / "bookstai_00001.png")
    assert result.negative_prompt == ""
    assert fake_client.last_post_payload == {
        "prompt": {
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": "a cinematic book cover"},
            }
        }
    }
    assert fake_client.last_bytes_url == "http://127.0.0.1:8188/view?filename=bookstai_00001.png&subfolder=&type=output"
    assert (tmp_path / "images" / "bookstai_00001.png").read_bytes() == b"PNGDATA"


def test_generate_handles_existing_image_path_fallback(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(post_response={"image_path": "outputs/images/generated.png"})
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    result = backend.generate(_request("prompt"))

    assert result.ok is True
    assert result.image_path == "outputs/images/generated.png"
    assert fake_client.last_bytes_url is None


def test_generate_raises_when_workflow_file_missing(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(
        workflow_path=tmp_path / "missing.json",
        output_dir=tmp_path / "images",
        http_client=FakeHTTPClient(),
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI workflow file not found."):
        backend.generate(_request("prompt"))


def test_generate_raises_when_workflow_json_is_invalid(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(
        workflow_path=_workflow_file(tmp_path, "{not json}"),
        output_dir=tmp_path / "images",
        http_client=FakeHTTPClient(),
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI workflow file is invalid JSON."):
        backend.generate(_request("prompt"))


def test_generate_raises_when_workflow_json_is_not_object(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(
        workflow_path=_workflow_file(tmp_path, "[]"),
        output_dir=tmp_path / "images",
        http_client=FakeHTTPClient(),
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI workflow must be a JSON object."):
        backend.generate(_request("prompt"))


def test_generate_raises_when_no_prompt_placeholder_exists(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path, """{"6": {"class_type": "SomethingElse", "inputs": {"text": "hello"}}}""")
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=FakeHTTPClient(post_response={"prompt_id": "abc123"}),
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI workflow does not contain a prompt placeholder."):
        backend.generate(_request("prompt"))


def test_generate_raises_when_prompt_id_is_missing(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(
        workflow_path=_workflow_file(tmp_path),
        output_dir=tmp_path / "images",
        http_client=FakeHTTPClient(post_response={}),
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI response did not contain a prompt id."):
        backend.generate(_request("prompt"))


def test_generate_raises_when_history_contains_invalid_image_reference(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {"9": {"images": [{"filename": "../evil.png", "subfolder": "", "type": "output"}]}}}}],
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI history contained an invalid image reference."):
        backend.generate(_request("prompt"))


@pytest.mark.parametrize("filename", ["..\\evil.png", "folder/evil.png", "folder\\evil.png", "C:\\temp\\evil.png", "/tmp/evil.png", ".", ".."])
def test_generate_rejects_dangerous_filenames(tmp_path: Path, filename: str) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {"9": {"images": [{"filename": filename, "subfolder": "", "type": "output"}]}}}}],
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI history contained an invalid image reference."):
        backend.generate(_request("prompt"))


def test_generate_raises_when_history_contains_dangerous_subfolder(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {"9": {"images": [{"filename": "image.png", "subfolder": "../secret", "type": "output"}]}}}}],
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    with pytest.raises(ImageGenerationError, match="ComfyUI history contained an invalid image reference."):
        backend.generate(_request("prompt"))


def test_generate_accepts_simple_filename(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {"9": {"images": [{"filename": "bookstai_00001.png", "subfolder": "", "type": "output"}]}}}}],
        bytes_response=b"PNGDATA",
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    result = backend.generate(_request("prompt"))

    assert result.image_path == str(tmp_path / "images" / "bookstai_00001.png")
    assert (tmp_path / "images" / "bookstai_00001.png").exists()


def test_generate_times_out_when_history_never_contains_image(monkeypatch, tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path)
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {}}}],
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        timeout=0.01,
        poll_interval=0.0,
        http_client=fake_client,
    )

    times = iter([0.0, 0.0, 0.02])
    monkeypatch.setattr("bookstai.image.comfyui_backend.time.sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr("bookstai.image.comfyui_backend.time.monotonic", lambda: next(times))

    with pytest.raises(ImageGenerationError, match="ComfyUI image generation timed out."):
        backend.generate(_request("prompt"))


def test_backend_uses_comfyui_http_client_by_default(tmp_path: Path) -> None:
    backend = ComfyUIImageBackend(output_dir=tmp_path / "images")

    assert isinstance(backend.http_client, ComfyUIHTTPClient)


def test_generate_supports_placeholder_injection_without_exact_node_match(tmp_path: Path) -> None:
    workflow_path = _workflow_file(tmp_path, """{"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "placeholder"}}}""")
    fake_client = FakeHTTPClient(
        post_response={"prompt_id": "abc123"},
        get_responses=[{"abc123": {"outputs": {"9": {"images": [{"filename": "image.png", "subfolder": "sub"}]}}}}],
        bytes_response=b"PNGDATA",
    )
    backend = ComfyUIImageBackend(
        workflow_path=workflow_path,
        output_dir=tmp_path / "images",
        http_client=fake_client,
    )

    result = backend.generate(_request("prompt"))

    assert result.image_path == str(tmp_path / "images" / "sub" / "image.png")
    assert fake_client.last_post_payload["prompt"]["6"]["inputs"]["text"] == "prompt"
