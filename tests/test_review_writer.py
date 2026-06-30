"""Tests for ReviewWriterAgent."""

from pathlib import Path

import pytest

from bookstai.agents.review_writer import ReviewWriterAgent
from bookstai.core.errors import PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_review_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Book: {{book_context}}\nStyle: {{style_context}}\nComedy: {{comedy_bank}}\nOpinion: {{user_opinion}}",
        encoding="utf-8",
    )

    agent = ReviewWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Review générée"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé du livre"}},
        style_context={"humor": {"references": "Humour de Céline"}},
        comedy_bank={"response": "Hooks et punchlines"},
        user_opinion="J’ai adoré le livre mais j’ai souffert.",
    )

    assert result["agent"] == "review_writer"
    assert result["prompt_path"] == "agents/review_writer.md"
    assert result["response"] == "Review générée"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{book_context}}", encoding="utf-8")

    agent = ReviewWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock review"),
    )

    result = agent.generate(
        book_context={"a": 1},
        style_context={"b": 2},
        comedy_bank={"c": 3},
        user_opinion="Bonne lecture",
    )

    assert result["response"] == "Mock review"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = ReviewWriterAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            book_context={},
            style_context={},
            comedy_bank={},
            user_opinion="Test",
        )


def test_agent_works_with_dict_contexts(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Book: {{book_context}}", encoding="utf-8")

    agent = ReviewWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé"}},
        style_context={"reviews": {"Tone": "Warm"}},
        comedy_bank={"response": "Ideas"},
        user_opinion="J’ai aimé.",
    )

    assert result == {
        "agent": "review_writer",
        "prompt_path": "agents/review_writer.md",
        "response": "OK",
    }


def test_agent_accepts_user_opinion_string(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Opinion: {{user_opinion}}", encoding="utf-8")

    agent = ReviewWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={},
        style_context={},
        comedy_bank={},
        user_opinion="Très bon livre",
    )

    assert result["response"] == "OK"
