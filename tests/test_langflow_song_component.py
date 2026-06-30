"""Tests for the Langflow song adapter."""

from pathlib import Path

from bookstai.langflow.song_component import run_song_workflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_run_song_workflow_returns_complete_result(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    result = run_song_workflow(
        book_slug="example",
        spoiler_mode="spoiler_free",
        prompt_type="thumbnail",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
        image_path=str(tmp_path / "outputs" / "mock" / "image.png"),
    )

    assert isinstance(result, dict)
    assert result["workflow"] == "song"
    assert result["book_slug"] == "example"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "song" in result
    assert "art_direction" in result
    assert "image_prompt" in result
    assert "image" in result
    assert "social" in result
    assert result["social"]["platform"] == "tiktok"
