"""Tests for the LLM factory."""

from __future__ import annotations

import sys

import pytest

from bookstai.core.errors import UnsupportedProviderError
from bookstai.llm.factory import create_llm_client
from bookstai.llm.mock import MockLLMClient


def test_create_llm_client_returns_mock_without_openai(monkeypatch) -> None:
    monkeypatch.delitem(sys.modules, "openai", raising=False)

    client = create_llm_client(provider="mock")

    assert isinstance(client, MockLLMClient)


def test_create_llm_client_openai_transmits_configuration(monkeypatch) -> None:
    captured = {}

    class DummyOpenAILLMClient:
        def __init__(self, model: str, temperature: float) -> None:
            captured["model"] = model
            captured["temperature"] = temperature

    monkeypatch.setattr(
        "bookstai.llm.factory.OpenAILLMClient",
        DummyOpenAILLMClient,
    )

    client = create_llm_client(
        provider="openai",
        model="gpt-4o-mini",
        temperature=0.3,
    )

    assert isinstance(client, DummyOpenAILLMClient)
    assert captured["model"] == "gpt-4o-mini"
    assert captured["temperature"] == 0.3


@pytest.mark.parametrize("provider", ["anthropic", "ollama"])
def test_create_llm_client_rejects_supported_but_unavailable_providers(provider) -> None:
    with pytest.raises(UnsupportedProviderError) as exc_info:
        create_llm_client(provider=provider)  # type: ignore[arg-type]

    assert str(exc_info.value) == f"Provider '{provider}' is not supported yet."


def test_create_llm_client_rejects_unknown_provider() -> None:
    with pytest.raises(UnsupportedProviderError) as exc_info:
        create_llm_client(provider="whatever")  # type: ignore[arg-type]

    assert str(exc_info.value) == "Provider 'whatever' is not supported yet."


def test_factory_does_not_read_openai_api_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "should-not-be-used")
    client = create_llm_client(provider="mock")

    assert isinstance(client, MockLLMClient)
