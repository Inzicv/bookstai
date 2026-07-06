"""Tests for PitchWorkflow."""

from pathlib import Path

from bookstai.llm.mock import MockLLMClient
from bookstai.workflows.pitch import PitchWorkflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_pitch_workflow_runs_end_to_end(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    pitchs_file = memory_root / "pitchs" / "output" / "pitchs.md"
    pitchs_file.parent.mkdir(parents=True)
    pitchs_file.write_text("# CASTEL BOY de Eny heli\nPitch style", encoding="utf-8")
    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")

    workflow = PitchWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="### Pitch 1\nA\n\n### Pitch 2\nB\n\n### Pitch 3\nC"),
    )

    result = workflow.run(item_slug="alchemised", summary="Résumé fourni")

    assert result["workflow"] == "pitch"
    assert result["item_slug"] == "alchemised"
    assert result["summary"] == "Résumé fourni"
    assert "style" in result
    assert "review_pitchs" in result["style"]
    assert "pitch_options" in result
    assert "review" not in result
    assert "social" not in result


def test_pitch_workflow_run_with_hitl_adds_only_pitch_options(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")

    workflow = PitchWorkflow(
        memory_root=memory_root,
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="### Pitch 1\nA\n\n### Pitch 2\nB\n\n### Pitch 3\nC"),
    )

    result = workflow.run_with_hitl(item_slug="alchemised", summary="Résumé fourni")

    assert result["workflow"] == "pitch"
    assert [step["name"] for step in result["hitl"]["steps"]] == ["pitch_options"]
