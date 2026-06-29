"""Tests for PromptLoader."""

from pathlib import Path

import pytest

from bookstai.core.errors import EmptyPromptFileError, PromptFileNotFoundError
from bookstai.prompts.loader import PromptLoader


def test_load_existing_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("# Title\nPrompt content", encoding="utf-8")

    loader = PromptLoader(prompt_root=prompt_root)
    content = loader.load("agents/review_writer.md")

    assert content == "# Title\nPrompt content"


def test_load_supports_string_path(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt content", encoding="utf-8")

    loader = PromptLoader(prompt_root=prompt_root)
    content = loader.load("agents/review_writer.md")

    assert content == "Prompt content"


def test_load_supports_path_object(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt content", encoding="utf-8")

    loader = PromptLoader(prompt_root=prompt_root)
    content = loader.load(Path("agents/review_writer.md"))

    assert content == "Prompt content"


def test_missing_prompt_raises(tmp_path: Path) -> None:
    loader = PromptLoader(prompt_root=tmp_path / "prompts")

    with pytest.raises(PromptFileNotFoundError):
        loader.load("agents/review_writer.md")


def test_empty_prompt_raises(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("", encoding="utf-8")

    loader = PromptLoader(prompt_root=prompt_root)

    with pytest.raises(EmptyPromptFileError):
        loader.load("agents/review_writer.md")


def test_whitespace_only_prompt_raises(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("   \n\t  ", encoding="utf-8")

    loader = PromptLoader(prompt_root=prompt_root)

    with pytest.raises(EmptyPromptFileError):
        loader.load("agents/review_writer.md")


def test_loads_raw_markdown(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "review_writer.md"
    prompt_file.parent.mkdir(parents=True)
    markdown = "# Heading\n\n- item 1\n- item 2"
    prompt_file.write_text(markdown, encoding="utf-8")

    loader = PromptLoader(prompt_root=prompt_root)
    content = loader.load("agents/review_writer.md")

    assert content == markdown
