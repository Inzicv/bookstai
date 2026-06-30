"""Tests for SongWorkflow."""

from pathlib import Path

import pytest

from bookstai.core.errors import MemoryFileNotFoundError, PromptFileNotFoundError
from bookstai.image.mock_backend import MockImageBackend
from bookstai.llm.mock import MockLLMClient
from bookstai.workflows.song import SongWorkflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_song_workflow_runs_end_to_end(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Image prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
        image_backend=MockImageBackend(image_path="outputs/mock/image.png"),
    )

    result = workflow.run(
        book_slug="alchemised",
        spoiler_mode="spoiler_free",
        prompt_type="scene",
        platform="instagram",
    )

    assert result["workflow"] == "song"
    assert result["book_slug"] == "alchemised"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "song" in result
    assert "art_direction" in result
    assert "image_prompt" in result
    assert "image" in result
    assert "social" in result
    assert result["image"]["image_path"] == "outputs/mock/image.png"
    assert result["social"]["platform"] == "instagram"


def test_song_workflow_propagates_missing_book_error(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Image prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = SongWorkflow(
        memory_root=tmp_path / "memory",
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
        image_backend=MockImageBackend(image_path="outputs/mock/image.png"),
    )

    with pytest.raises(MemoryFileNotFoundError):
        workflow.run(
            book_slug="alchemised",
            spoiler_mode="spoiler_free",
            prompt_type="scene",
            platform="instagram",
        )


def test_song_workflow_propagates_missing_prompt_error(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
        image_backend=MockImageBackend(image_path="outputs/mock/image.png"),
    )

    with pytest.raises(PromptFileNotFoundError):
        workflow.run(
            book_slug="alchemised",
            spoiler_mode="spoiler_free",
            prompt_type="scene",
            platform="instagram",
        )


def test_song_workflow_accepts_spoiler_free_scene_instagram(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Image prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
        image_backend=MockImageBackend(image_path="outputs/mock/image.png"),
    )

    result = workflow.run(
        book_slug="alchemised",
        spoiler_mode="spoiler_free",
        prompt_type="scene",
        platform="instagram",
    )

    assert result["song"]["spoiler_mode"] == "spoiler_free"
    assert result["image_prompt"]["prompt_type"] == "scene"
    assert result["social"]["platform"] == "instagram"
