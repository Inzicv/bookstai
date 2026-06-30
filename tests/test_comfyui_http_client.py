"""Tests for ComfyUI HTTP client."""

from __future__ import annotations

import json
from urllib import error

import pytest

from bookstai.core.errors import ImageBackendConnectionError
from bookstai.image.comfyui_backend import ComfyUIHTTPClient


class FakeResponse:
    def __init__(self, body: str) -> None:
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return self.body.encode("utf-8")


def test_post_json_makes_post_request(monkeypatch) -> None:
    captured = {}

    def fake_urlopen(req, timeout):
        captured["method"] = req.method
        captured["url"] = req.full_url
        captured["data"] = req.data
        captured["headers"] = req.headers
        captured["timeout"] = timeout
        return FakeResponse(json.dumps({"ok": True}))

    monkeypatch.setattr("bookstai.image.comfyui_backend.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()
    result = client.post_json("http://example.test/prompt", {"prompt": "hello"}, timeout=12.5)

    assert result == {"ok": True}
    assert captured["method"] == "POST"
    assert captured["url"] == "http://example.test/prompt"
    assert json.loads(captured["data"].decode("utf-8")) == {"prompt": "hello"}
    assert captured["timeout"] == 12.5


def test_post_json_rejects_non_dict_json(monkeypatch) -> None:
    monkeypatch.setattr("bookstai.image.comfyui_backend.request.urlopen", lambda req, timeout: FakeResponse("[]"))

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.post_json("http://example.test/prompt", {"prompt": "hello"}, timeout=1.0)


def test_post_json_converts_network_errors(monkeypatch) -> None:
    def fake_urlopen(req, timeout):
        raise error.URLError("boom")

    monkeypatch.setattr("bookstai.image.comfyui_backend.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.post_json("http://example.test/prompt", {"prompt": "hello"}, timeout=1.0)


def test_get_json_makes_get_request(monkeypatch) -> None:
    captured = {}

    def fake_urlopen(req, timeout):
        captured["method"] = req.method
        captured["url"] = req.full_url
        captured["timeout"] = timeout
        return FakeResponse(json.dumps({"history": True}))

    monkeypatch.setattr("bookstai.image.comfyui_backend.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()
    result = client.get_json("http://example.test/history/abc123", timeout=8.0)

    assert result == {"history": True}
    assert captured["method"] == "GET"
    assert captured["url"] == "http://example.test/history/abc123"
    assert captured["timeout"] == 8.0


def test_get_json_rejects_non_dict_json(monkeypatch) -> None:
    monkeypatch.setattr("bookstai.image.comfyui_backend.request.urlopen", lambda req, timeout: FakeResponse("[]"))

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.get_json("http://example.test/history/abc123", timeout=1.0)


def test_get_json_converts_network_errors(monkeypatch) -> None:
    def fake_urlopen(req, timeout):
        raise error.URLError("boom")

    monkeypatch.setattr("bookstai.image.comfyui_backend.request.urlopen", fake_urlopen)

    client = ComfyUIHTTPClient()

    with pytest.raises(ImageBackendConnectionError):
        client.get_json("http://example.test/history/abc123", timeout=1.0)
