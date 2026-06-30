"""Tests for ReviewWorkflow."""

from pathlib import Path

import pytest

from bookstai.core.errors import MemoryFileNotFoundError, PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient
from bookstai.workflows.review import ReviewWorkflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_review_workflow_runs_end_to_end(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = ReviewWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    result = workflow.run(
        book_slug="alchemised",
        user_opinion="J’ai adoré mais j’ai souffert.",
        platform="instagram",
    )

    assert result["workflow"] == "review"
    assert result["book_slug"] == "alchemised"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "review" in result
    assert "social" in result
    assert result["social"]["platform"] == "instagram"
    assert "hitl" not in result


def test_review_workflow_propagates_missing_book_error(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = ReviewWorkflow(
        memory_root=tmp_path / "memory",
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    with pytest.raises(MemoryFileNotFoundError):
        workflow.run(
            book_slug="alchemised",
            user_opinion="J’ai adoré mais j’ai souffert.",
            platform="instagram",
        )


def test_review_workflow_propagates_missing_prompt_error(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")

    workflow = ReviewWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    with pytest.raises(PromptFileNotFoundError):
        workflow.run(
            book_slug="alchemised",
            user_opinion="J’ai adoré mais j’ai souffert.",
            platform="instagram",
        )


def test_review_workflow_works_with_instagram_platform(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = ReviewWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    result = workflow.run(
        book_slug="alchemised",
        user_opinion="J’ai adoré mais j’ai souffert.",
        platform="instagram",
    )

    assert result["social"]["platform"] == "instagram"


def test_review_workflow_run_with_hitl_returns_hitl_session(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Résumé\nRésumé du livre", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    workflow = ReviewWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Réponse mock"),
    )

    result = workflow.run_with_hitl(
        book_slug="alchemised",
        user_opinion="J’ai adoré mais j’ai souffert.",
        platform="instagram",
    )

    assert result["workflow"] == "review"
    assert "hitl" in result
    assert result["hitl"]["workflow_name"] == "review"
    assert result["hitl"]["item_slug"] == "alchemised"
    assert [step["name"] for step in result["hitl"]["steps"]] == ["comedy", "review", "social"]
    assert all(step["status"] == "pending" for step in result["hitl"]["steps"])
    assert result["hitl"]["steps"][0]["content"] == result["comedy"]
    assert result["hitl"]["steps"][1]["content"] == result["review"]
    assert result["hitl"]["steps"][2]["content"] == result["social"]
    assert "context" not in [step["name"] for step in result["hitl"]["steps"]]
    assert "style" not in [step["name"] for step in result["hitl"]["steps"]]
