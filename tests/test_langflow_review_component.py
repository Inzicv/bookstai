"""Tests for the Langflow review adapter."""

from pathlib import Path

from bookstai.langflow.review_component import run_review_workflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_run_review_workflow_returns_complete_result(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    result = run_review_workflow(
        book_slug="example",
        user_opinion="J'ai aimé l'ambiance et les personnages.",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
    )

    assert isinstance(result, dict)
    assert result["workflow"] == "review"
    assert result["book_slug"] == "example"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "review" in result
    assert "social" in result
    assert result["social"]["platform"] == "tiktok"
