"""Tests for the BookstAI project pre-check."""

from __future__ import annotations

from pathlib import Path

from bookstai.precheck import REQUIRED_AGENT_PROMPTS, check_required_agent_prompts
from bookstai.llm.mock import MockLLMClient
from bookstai.image.mock_backend import MockImageBackend
from bookstai.workflows.review import ReviewWorkflow
from bookstai.workflows.song import SongWorkflow


def _write_required_prompts(prompt_root: Path, names: list[str]) -> None:
    for name in names:
        prompt_file = prompt_root / name
        prompt_file.parent.mkdir(parents=True, exist_ok=True)
        prompt_file.write_text(f"# {name}\n", encoding="utf-8")


def test_precheck_returns_ok_when_all_required_prompts_exist(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    _write_required_prompts(prompt_root, REQUIRED_AGENT_PROMPTS)

    result = check_required_agent_prompts(prompt_root=prompt_root)

    assert result["ok"] is True
    assert result["missing_prompts"] == []


def test_precheck_reports_missing_prompts(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    _write_required_prompts(prompt_root, REQUIRED_AGENT_PROMPTS[:3])

    result = check_required_agent_prompts(prompt_root=prompt_root)

    assert result["ok"] is False
    assert result["missing_prompts"] == REQUIRED_AGENT_PROMPTS[3:]


def test_precheck_uses_default_prompt_root() -> None:
    result = check_required_agent_prompts()

    assert "ok" in result
    assert isinstance(result["prompt_root"], str)


def test_agent_prompt_files_exist_in_project() -> None:
    project_root = Path(__file__).resolve().parents[1]
    prompt_root = project_root / "prompts"

    for relative_path in REQUIRED_AGENT_PROMPTS:
        prompt_file = prompt_root / relative_path
        assert prompt_file.exists()
        assert prompt_file.read_text(encoding="utf-8").strip()


def test_agent_prompt_files_contain_expected_variables() -> None:
    project_root = Path(__file__).resolve().parents[1]
    prompt_root = project_root / "prompts"
    expected_variables = {
        "comedy_room.md": {"book_context", "style_context"},
        "review_writer.md": {"book_context", "style_context", "comedy_bank", "user_opinion"},
        "song_writer.md": {"book_context", "style_context", "comedy_bank", "spoiler_mode"},
        "art_director.md": {"book_context", "style_context", "validated_content"},
        "prompt_maker.md": {"art_direction", "prompt_type"},
        "social_media.md": {"validated_content", "style_context", "platform"},
        "memory_manager.md": {"generated_content", "corrected_content"},
    }

    allowed_variables = {
        "comedy_room.md": {"book_context", "style_context"},
        "review_writer.md": {"book_context", "style_context", "comedy_bank", "user_opinion"},
        "song_writer.md": {"book_context", "style_context", "comedy_bank", "spoiler_mode"},
        "art_director.md": {"book_context", "style_context", "validated_content"},
        "prompt_maker.md": {"art_direction", "prompt_type"},
        "social_media.md": {"validated_content", "style_context", "platform"},
        "memory_manager.md": {"generated_content", "corrected_content"},
    }

    for filename, expected in expected_variables.items():
        content = (prompt_root / "agents" / filename).read_text(encoding="utf-8")
        for variable in expected:
            assert f"{{{{{variable}}}}}" in content

        allowed = allowed_variables[filename]
        import re

        found = set(re.findall(r"{{\s*([a-zA-Z0-9_]+)\s*}}", content))
        assert found <= allowed


def test_agent_prompt_files_include_bookstai_editorial_identity() -> None:
    project_root = Path(__file__).resolve().parents[1]
    prompt_root = project_root / "prompts"
    creative_prompts = [
        "comedy_room.md",
        "review_writer.md",
        "song_writer.md",
        "art_director.md",
        "prompt_maker.md",
        "social_media.md",
    ]

    for filename in creative_prompts:
        content = (prompt_root / "agents" / filename).read_text(encoding="utf-8").lower()
        assert "bookstai" in content
        assert "human in the loop" in content
        assert "créatrice" in content or "creator" in content
        if filename != "prompt_maker.md":
            assert "style_context" in content


def test_project_review_workflow_can_run_with_real_prompts_and_mock(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    project_root = Path(__file__).resolve().parents[1]
    prompt_root = project_root / "prompts"

    workflow = ReviewWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(),
    )

    result = workflow.run(
        book_slug="example",
        user_opinion="J'ai aimé l'ambiance.",
        platform="tiktok",
    )

    assert result["workflow"] == "review"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "review" in result
    assert "social" in result


def test_project_song_workflow_can_run_with_real_prompts_and_mock(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    project_root = Path(__file__).resolve().parents[1]
    prompt_root = project_root / "prompts"

    workflow = SongWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(),
        image_backend=MockImageBackend(image_path="outputs/mock/image.png"),
    )

    result = workflow.run(
        book_slug="example",
        spoiler_mode="spoiler_free",
        prompt_type="thumbnail",
        platform="tiktok",
    )

    assert result["workflow"] == "song"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "song" in result
    assert "art_direction" in result
    assert "image_prompt" in result
    assert "image" in result
    assert "social" in result
