"""Tests for SongWorkflow."""

from pathlib import Path

import pytest

from bookstai.core.errors import MemoryFileNotFoundError, PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient
from bookstai.workflows.song import SongWorkflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(content, encoding="utf-8")


def _prepare_prompts(prompt_root: Path) -> None:
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Prompts: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")


def _prepare_memory(memory_root: Path) -> None:
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")


def test_song_workflow_runs_end_to_end(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    _prepare_memory(memory_root)
    prompt_root = tmp_path / "prompts"
    _prepare_prompts(prompt_root)

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    result = workflow.run(
        book_slug="alchemised",
        story_scope="pitch_only",
        song_style="parody",
        platform="instagram",
    )

    assert result["workflow"] == "song"
    assert result["book_slug"] == "alchemised"
    assert result["story_scope"] == "pitch_only"
    assert result["song_style"] == "parody"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "song" in result
    assert "storyboard" in result
    assert "prompts" in result
    assert "social" in result
    assert "image" not in result
    assert result["song"]["story_scope"] == "pitch_only"
    assert result["social"]["platform"] == "instagram"


def test_song_workflow_propagates_missing_book_error(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    _prepare_prompts(prompt_root)

    workflow = SongWorkflow(
        memory_root=tmp_path / "memory",
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    with pytest.raises(MemoryFileNotFoundError):
        workflow.run(
            book_slug="alchemised",
            story_scope="pitch_only",
            song_style="parody",
            platform="instagram",
        )


def test_song_workflow_propagates_missing_prompt_error(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    _prepare_memory(memory_root)
    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    with pytest.raises(PromptFileNotFoundError):
        workflow.run(
            book_slug="alchemised",
            story_scope="pitch_only",
            song_style="parody",
            platform="instagram",
        )


def test_song_workflow_run_with_hitl_returns_hitl_session(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    _prepare_memory(memory_root)
    prompt_root = tmp_path / "prompts"
    _prepare_prompts(prompt_root)

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    result = workflow.run_with_hitl(
        book_slug="alchemised",
        story_scope="full_spoilers",
        song_style="parody",
        platform="instagram",
    )

    assert result["workflow"] == "song"
    assert "hitl" in result
    assert result["hitl"]["workflow_name"] == "song"
    assert result["hitl"]["item_slug"] == "alchemised"
    assert [step["name"] for step in result["hitl"]["steps"]] == [
        "comedy",
        "song",
        "storyboard",
        "prompts",
        "social",
    ]
    assert all(step["status"] == "pending" for step in result["hitl"]["steps"])
    assert result["hitl"]["steps"][0]["content"] == result["comedy"]
    assert result["hitl"]["steps"][1]["content"] == result["song"]
    assert result["hitl"]["steps"][2]["content"] == result["storyboard"]
    assert result["hitl"]["steps"][3]["content"] == result["prompts"]
    assert result["hitl"]["steps"][4]["content"] == result["social"]
