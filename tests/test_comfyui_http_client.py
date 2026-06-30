"""Tests for the ComfyUI HTTP client."""

from __future__ import annotations

import json
from urllib import error

import pytest

from bookstai.core.errors import ImageBackendConnectionError
from bookstai.image.comfyui_backend import ComfyUIHTTPClient


class FakeHTTPResponse:
    def __init__(self, body: str) -> None:
        self._body = body.encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_comfyui_http_client_can_be_imported() -> None:
    assert ComfyUIHTTPClient is not None


def test_post_json_sends_post_json_request(monkeypatch) -> None:
    captured = {}

    def fake_urlopen(req, timeout):
        captured["method"] = req.get_method()
        captured["headers"] = dict(req.headers)
        captured["timeout"] = timeout
        captured["data"] = json.loads(req.data.decode("utf-8"))
        return FakeHTTPResponse('{"image_path": "outputs/images/generated.png"}')

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()
    result = client.post_json(
        "http://127.0.0.1:8188/prompt",
        {"prompt": "a cinematic book cover"},
        timeout=12.5,
    )

    assert captured["method"] == "POST"
    assert captured["headers"]["Content-type"] == "application/json"
    assert captured["timeout"] == 12.5
    assert captured["data"] == {"prompt": "a cinematic book cover"}
    assert result == {"image_path": "outputs/images/generated.png"}


def test_post_json_raises_on_network_error(monkeypatch) -> None:
    def fake_urlopen(req, timeout):
        raise error.URLError("unreachable")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.post_json("http://127.0.0.1:8188/prompt", {"prompt": "x"}, timeout=1.0)


def test_post_json_raises_on_invalid_json(monkeypatch) -> None:
    def fake_urlopen(req, timeout):
        return FakeHTTPResponse("not-json")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.post_json("http://127.0.0.1:8188/prompt", {"prompt": "x"}, timeout=1.0)


def test_post_json_raises_when_json_is_not_dict(monkeypatch) -> None:
    def fake_urlopen(req, timeout):
        return FakeHTTPResponse("[1, 2, 3]")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.post_json("http://127.0.0.1:8188/prompt", {"prompt": "x"}, timeout=1.0)
