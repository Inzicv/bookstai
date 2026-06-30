"""Tests for PromptBuilder."""

from pathlib import Path

import pytest

from bookstai.core.errors import (
    EmptyPromptFileError,
    MissingPromptVariableError,
    PromptFileNotFoundError,
)
from bookstai.prompts.builder import PromptBuilder


def test_build_valid_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Livre : {{book_title}}\nContexte : {{book_context}}",
        encoding="utf-8",
    )

    builder = PromptBuilder(prompt_root=prompt_root)
    result = builder.build(
        prompt_path="agents/review_writer.md",
        variables={
            "book_title": "Alchemised",
            "book_context": "Contexte du livre",
        },
    )

    assert result == "Livre : Alchemised\nContexte : Contexte du livre"


def test_build_supports_string_path(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Titre: {{title}}", encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)
    result = builder.build("agents/review_writer.md", {"title": "Alchemised"})

    assert result == "Titre: Alchemised"


def test_build_supports_path_object(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Titre: {{title}}", encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)
    result = builder.build(Path("agents/review_writer.md"), {"title": "Alchemised"})

    assert result == "Titre: Alchemised"


def test_build_converts_non_string_values(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Pages: {{pages}}", encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)
    result = builder.build("agents/review_writer.md", {"pages": 432})

    assert result == "Pages: 432"


def test_missing_prompt_file_error_propagates(tmp_path: Path) -> None:
    builder = PromptBuilder(prompt_root=tmp_path / "prompts")

    with pytest.raises(PromptFileNotFoundError):
        builder.build("agents/review_writer.md", {})


def test_empty_prompt_file_error_propagates(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("", encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)

    with pytest.raises(EmptyPromptFileError):
        builder.build("agents/review_writer.md", {})


def test_missing_variable_error_propagates(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Livre : {{book_title}}", encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)

    with pytest.raises(MissingPromptVariableError):
        builder.build("agents/review_writer.md", {})


def test_empty_prompt_template_error_propagates(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("   \n\t ", encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)

    with pytest.raises(EmptyPromptFileError):
        builder.build("agents/review_writer.md", {"x": "y"})


def test_preserves_raw_markdown_outside_variables(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    markdown = "# Heading\n\n- item 1\n- item 2"
    prompt_file.write_text(markdown, encoding="utf-8")

    builder = PromptBuilder(prompt_root=prompt_root)
    result = builder.build("agents/review_writer.md", {})

    assert result == markdown
