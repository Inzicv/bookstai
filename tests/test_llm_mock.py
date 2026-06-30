"""Tests for the mock LLM client."""

import pytest

from bookstai.core.errors import EmptyPromptError
from bookstai.llm.client import LLMClient
from bookstai.llm.mock import DEFAULT_RESPONSE, MockLLMClient


def test_mock_returns_configured_response() -> None:
    client = MockLLMClient(response="Réponse test")

    assert client.generate("Hello") == "Réponse test"


def test_mock_returns_default_response() -> None:
    client = MockLLMClient()

    assert client.generate("Hello") == DEFAULT_RESPONSE


def test_generate_accepts_valid_prompt() -> None:
    client = MockLLMClient(response="OK")

    assert client.generate("Prompt test") == "OK"


@pytest.mark.parametrize("prompt", ["", "   ", "\t\n"])
def test_generate_raises_for_empty_prompt(prompt: str) -> None:
    client = MockLLMClient()

    with pytest.raises(EmptyPromptError):
        client.generate(prompt)


def test_mock_respects_llm_client_interface() -> None:
    client: LLMClient = MockLLMClient(response="Interface OK")

    assert client.generate("Prompt") == "Interface OK"
