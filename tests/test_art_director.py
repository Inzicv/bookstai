"""Tests for ArtDirectorAgent."""

from pathlib import Path

import pytest

from bookstai.agents.art_director import ArtDirectorAgent
from bookstai.core.errors import PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_art_director_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "art_director.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Book: {{book_context}}\nStyle: {{style_context}}\nContent: {{validated_content}}",
        encoding="utf-8",
    )

    agent = ArtDirectorAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Direction artistique"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé du livre"}},
        style_context={"visual_style": {"paper": "Style diorama"}},
        validated_content="Paroles validées ou contenu validé",
    )

    assert result["agent"] == "art_director"
    assert result["prompt_path"] == "agents/art_director.md"
    assert result["response"] == "Direction artistique"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "art_director.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{book_context}}", encoding="utf-8")

    agent = ArtDirectorAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock art direction"),
    )

    result = agent.generate(
        book_context={"a": 1},
        style_context={"b": 2},
        validated_content="Contenu validé",
    )

    assert result["response"] == "Mock art direction"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = ArtDirectorAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            book_context={},
            style_context={},
            validated_content="Contenu validé",
        )


def test_agent_works_with_dict_contexts(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "art_director.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Book: {{book_context}}", encoding="utf-8")

    agent = ArtDirectorAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé"}},
        style_context={"visual_style": {"paper": "Diorama"}},
        validated_content="Texte validé",
    )

    assert result == {
        "agent": "art_director",
        "prompt_path": "agents/art_director.md",
        "response": "OK",
    }


def test_agent_accepts_validated_content_string(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "art_director.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Content: {{validated_content}}", encoding="utf-8")

    agent = ArtDirectorAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={},
        style_context={},
        validated_content="Paroles validées",
    )

    assert result["response"] == "OK"
