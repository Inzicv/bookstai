"""Tests for ContextBuilder."""

from pathlib import Path

import pytest

from bookstai.agents.context_builder import ContextBuilder
from bookstai.core.errors import MemoryFileNotFoundError


def test_build_constructs_book_path(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Titre\nContenu", encoding="utf-8")

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "review", "light")

    assert context["source_path"] == str(book_file)


def test_build_uses_file_in_memory_books(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Titre\n\n# Auteur\n", encoding="utf-8")

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "review", "full")

    assert "Titre" in context["sections"]
    assert "Auteur" in context["sections"]


def test_build_keeps_workflow_and_spoiler_metadata(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Titre\nContenu", encoding="utf-8")

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "review", "light")

    assert context["workflow_type"] == "review"
    assert context["spoiler_level"] == "light"


def test_missing_file_error_propagates(tmp_path: Path) -> None:
    builder = ContextBuilder(memory_root=tmp_path / "memory")

    with pytest.raises(MemoryFileNotFoundError):
        builder.build("alchemised", "review", "light")
