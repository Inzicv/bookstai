"""Tests for ComedyRoomAgent."""

from pathlib import Path

import pytest

from bookstai.core.errors import PromptFileNotFoundError
from bookstai.agents.comedy_room import ComedyRoomAgent
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_comedy_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "comedy_room.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Book: {{book_context}}\nStyle: {{style_context}}",
        encoding="utf-8",
    )

    agent = ComedyRoomAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse humour"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé du livre"}},
        style_context={"humor": {"references": "Humour de Céline"}},
    )

    assert result["agent"] == "comedy_room"
    assert result["prompt_path"] == "agents/comedy_room.md"
    assert result["response"] == "Réponse humour"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "comedy_room.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{book_context}}", encoding="utf-8")

    agent = ComedyRoomAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock output"),
    )

    result = agent.generate(book_context={"a": 1}, style_context={"b": 2})

    assert result["response"] == "Mock output"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = ComedyRoomAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(book_context={}, style_context={})


def test_agent_works_with_dict_contexts(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "comedy_room.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Book: {{book_context}}", encoding="utf-8")

    agent = ComedyRoomAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé"}},
        style_context={"reviews": {"Tone": "Warm"}},
    )

    assert result == {
        "agent": "comedy_room",
        "prompt_path": "agents/comedy_room.md",
        "response": "OK",
    }
