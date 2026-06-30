"""Tests for OpenAILLMClient."""

from __future__ import annotations

import importlib
import sys
from types import SimpleNamespace

import pytest

from bookstai.core.errors import EmptyPromptError, MissingAPIKeyError
from bookstai.llm.openai_client import OpenAILLMClient


class DummyResponses:
    def __init__(self, response: object) -> None:
        self.response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class DummyOpenAI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.responses = DummyResponses(
            SimpleNamespace(output_text="mocked text", output=[])
        )


def test_openai_client_can_be_imported() -> None:
    module = importlib.import_module("bookstai.llm")
    assert hasattr(module, "OpenAILLMClient")


def test_openai_client_requires_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(MissingAPIKeyError) as exc_info:
        OpenAILLMClient(api_key=None)

    assert "OPENAI_API_KEY" in str(exc_info.value)
    assert "secret" not in str(exc_info.value).lower()


def test_openai_client_accepts_explicit_api_key(monkeypatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=DummyOpenAI),
    )

    client = OpenAILLMClient(api_key="explicit-key")

    assert not hasattr(client, "api_key")


def test_openai_client_accepts_env_api_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=DummyOpenAI),
    )

    client = OpenAILLMClient()

    assert not hasattr(client, "api_key")


def test_generate_rejects_empty_prompt(monkeypatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=DummyOpenAI),
    )
    client = OpenAILLMClient(api_key="key")

    with pytest.raises(EmptyPromptError):
        client.generate("")


def test_generate_returns_output_text(monkeypatch) -> None:
    response = SimpleNamespace(output_text="Generated review", output=[])
    dummy_openai = SimpleNamespace(OpenAI=lambda api_key: SimpleNamespace(responses=DummyResponses(response)))
    monkeypatch.setitem(sys.modules, "openai", dummy_openai)

    client = OpenAILLMClient(api_key="key", model="gpt-test", temperature=0.3)
    result = client.generate("Hello")

    assert result == "Generated review"
    assert client._client.responses.calls[0]["model"] == "gpt-test"
    assert client._client.responses.calls[0]["temperature"] == 0.3
    assert client._client.responses.calls[0]["input"] == "Hello"


def test_generate_raises_clear_error_when_no_text(monkeypatch) -> None:
    response = SimpleNamespace(output_text="", output=[])
    dummy_openai = SimpleNamespace(OpenAI=lambda api_key: SimpleNamespace(responses=DummyResponses(response)))
    monkeypatch.setitem(sys.modules, "openai", dummy_openai)

    client = OpenAILLMClient(api_key="key")

    with pytest.raises(ValueError):
        client.generate("Hello")


def test_error_messages_do_not_reveal_api_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "super-secret-key")
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=DummyOpenAI),
    )

    client = OpenAILLMClient()

    assert not hasattr(client, "api_key")


def test_missing_api_key_error_message_does_not_reveal_secret(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(MissingAPIKeyError) as exc_info:
        OpenAILLMClient(api_key=None)

    assert "super-secret-key" not in str(exc_info.value)
