"""Tests for SongWriterAgent."""

from pathlib import Path

import pytest

from bookstai.agents.song_writer import SongWriterAgent
from bookstai.core.errors import InvalidSpoilerModeError, PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_song_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "song_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Book: {{book_context}}\nStyle: {{style_context}}\nComedy: {{comedy_bank}}\nScope: {{story_scope}}",
        encoding="utf-8",
    )

    agent = SongWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Paroles générées"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé du livre"}},
        style_context={"songs": {"old_song": {"lyrics": "Ancienne chanson"}}},
        comedy_bank={"response": "Hooks et punchlines"},
        story_scope="pitch_only",
        song_style="parody",
    )

    assert result["agent"] == "song_writer"
    assert result["prompt_path"] == "agents/song_writer.md"
    assert result["story_scope"] == "pitch_only"
    assert result["title"] == "BookstAI Song"
    assert result["response"] == "Paroles générées"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "song_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{book_context}}", encoding="utf-8")

    agent = SongWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock lyrics"),
    )

    result = agent.generate(
        book_context={"a": 1},
        style_context={"b": 2},
        comedy_bank={"c": 3},
        story_scope="full_spoilers",
        song_style="parody",
    )

    assert result["response"] == "Mock lyrics"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = SongWriterAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            book_context={},
            style_context={},
            comedy_bank={},
            story_scope="pitch_only",
            song_style="parody",
        )


def test_agent_works_with_dict_contexts(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "song_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Book: {{book_context}}", encoding="utf-8")

    agent = SongWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={"sections": {"résumé": "Résumé"}},
        style_context={"reviews": {"Tone": "Warm"}},
        comedy_bank={"response": "Ideas"},
        story_scope="full_spoilers",
        song_style="parody",
    )

    assert result["agent"] == "song_writer"
    assert result["story_scope"] == "full_spoilers"
    assert result["spoiler_mode"] == "full"


def test_agent_accepts_legacy_spoiler_mode(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "song_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Mode: {{story_scope}}", encoding="utf-8")

    agent = SongWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        book_context={},
        style_context={},
        comedy_bank={},
        spoiler_mode="spoiler_free",
    )

    assert result["story_scope"] == "pitch_only"


def test_agent_raises_invalid_spoiler_mode_error(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "song_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Mode: {{story_scope}}", encoding="utf-8")

    agent = SongWriterAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    with pytest.raises(InvalidSpoilerModeError):
        agent.generate(
            book_context={},
            style_context={},
            comedy_bank={},
            story_scope="partial",
            song_style="parody",
        )
