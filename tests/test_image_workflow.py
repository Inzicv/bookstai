"""Tests for ImageWorkflow."""

from __future__ import annotations

from pathlib import Path

from bookstai.llm.mock import MockLLMClient
from bookstai.workflows.image import ImageWorkflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def _write_book(memory_root: Path, slug: str = "alchemised") -> None:
    book_file = memory_root / "books" / f"{slug}.md"
    book_file.parent.mkdir(parents=True, exist_ok=True)
    book_file.write_text("# Book\nContenu de test.", encoding="utf-8")


def _write_style(memory_root: Path) -> None:
    style_file = memory_root / "visual_style" / "Prompts_visuels" / "lego.md"
    style_file.parent.mkdir(parents=True, exist_ok=True)
    style_file.write_text(
        """---
id: lego
name: Lego
---
# Lego
Instructions de style.
""",
        encoding="utf-8",
    )


class DummyArtDirector:
    def __init__(self, *args, **kwargs) -> None:
        self.calls = []

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        return {"storyboard": [{"shot_number": 1}], "response": "storyboard"}


class DummyPromptMaker:
    def __init__(self, *args, **kwargs) -> None:
        self.calls = []

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        return {"prompts": [{"name": "p1"}], "response": "prompts"}


def test_image_workflow_runs_with_book_context(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    prompt_root = tmp_path / "prompts"
    _write_book(memory_root)
    _write_style(memory_root)
    _write_prompt(prompt_root, "art_director.md", "Book: {{book_context}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Book: {{book_context}}")

    art_director = DummyArtDirector()
    prompt_maker = DummyPromptMaker()
    monkeypatch.setattr("bookstai.workflows.image.ArtDirectorAgent", lambda *args, **kwargs: art_director)
    monkeypatch.setattr("bookstai.workflows.image.PromptMakerAgent", lambda *args, **kwargs: prompt_maker)

    workflow = ImageWorkflow(memory_root=memory_root, prompt_root=prompt_root, llm_client=MockLLMClient())
    result = workflow.run(
        book_slug="alchemised",
        lyrics="Paroles validées",
        visual_style_id="lego",
    )

    assert result["book_slug"] == "alchemised"
    assert result["book_context"]["book_slug"] == "alchemised"
    assert result["workflow"] == "visual"
    assert result["style_selection"]["book_slug"] == "alchemised"
    assert result["item_slug"].startswith("alchemised-lego-")
    assert art_director.calls[0]["book_context"]["book_slug"] == "alchemised"
    assert prompt_maker.calls[0]["book_context"]["book_slug"] == "alchemised"
    assert prompt_maker.calls[0]["validated_storyboard"]["response"] == "storyboard"
    assert "storyboard" in result
    assert "prompts" in result


def test_image_workflow_run_with_hitl_includes_steps(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    prompt_root = tmp_path / "prompts"
    _write_book(memory_root)
    _write_style(memory_root)
    _write_prompt(prompt_root, "art_director.md", "Book: {{book_context}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Book: {{book_context}}")

    monkeypatch.setattr("bookstai.workflows.image.ArtDirectorAgent", lambda *args, **kwargs: DummyArtDirector())
    monkeypatch.setattr("bookstai.workflows.image.PromptMakerAgent", lambda *args, **kwargs: DummyPromptMaker())

    workflow = ImageWorkflow(memory_root=memory_root, prompt_root=prompt_root, llm_client=MockLLMClient())
    result = workflow.run_with_hitl(
        book_slug="alchemised",
        lyrics="Paroles validées",
        visual_style_id="lego",
    )

    assert result["book_slug"] == "alchemised"
    assert [step["name"] for step in result["hitl"]["steps"]] == ["style_selection", "storyboard", "prompts"]
