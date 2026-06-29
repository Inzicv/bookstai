"""Tests for ContextBuilder."""

from pathlib import Path

import pytest

from bookstai.agents.context_builder import ContextBuilder
from bookstai.core.errors import (
    InvalidSpoilerLevelError,
    InvalidWorkflowError,
    MemoryFileNotFoundError,
)


def test_build_constructs_book_path(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Titre\nContenu", encoding="utf-8")

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "review", "light")

    assert context["source_path"] == str(book_file)
    assert context["book_slug"] == "alchemised"
    assert context["workflow_type"] == "review"
    assert context["spoiler_level"] == "light"


def test_build_uses_file_in_memory_books(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Titre\n\n# Auteur\n", encoding="utf-8")

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "review", "full")

    assert "Titre" in context["sections"]
    assert "Auteur" in context["sections"]


def test_build_filters_review_workflow(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text(
        """# Titre
Book title

# Auteur
Author

# Personnages
Characters

# Tropes
Trope details

# R\u00e9sum\u00e9
Summary

# Avis
Review

# Ambiance
Mood

# Song Suggestions
Songs

# Lieux
Locations
""",
        encoding="utf-8",
    )

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "review", "full")

    assert set(context["sections"]) == {
        "Titre",
        "Auteur",
        "Personnages",
        "Tropes",
        "R\u00e9sum\u00e9",
        "Avis",
        "Ambiance",
        "Song Suggestions",
    }


def test_build_filters_spoiler_none(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text(
        """# R\u00e9sum\u00e9
Summary

# Timeline
Timeline

# \u00c9v\u00e9nements
Events

# Fin
Ending

# R\u00e9v\u00e9lation
Reveal

# Spoiler Alert
Spoilers

# Titre
Title
""",
        encoding="utf-8",
    )

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "song", "none")

    assert "R\u00e9sum\u00e9" in context["sections"]
    assert "Titre" in context["sections"]
    assert "Timeline" not in context["sections"]
    assert "\u00c9v\u00e9nements" not in context["sections"]
    assert "Fin" not in context["sections"]
    assert "R\u00e9v\u00e9lation" not in context["sections"]
    assert "Spoiler Alert" not in context["sections"]


def test_build_filters_spoiler_full(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "alchemised.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text(
        """# R\u00e9sum\u00e9
Summary

# Timeline
Timeline

# Fin
Ending
""",
        encoding="utf-8",
    )

    builder = ContextBuilder(memory_root=memory_root)
    context = builder.build("alchemised", "song", "full")

    assert set(context["sections"]) == {"R\u00e9sum\u00e9", "Timeline", "Fin"}


def test_invalid_workflow_raises(tmp_path: Path) -> None:
    builder = ContextBuilder(memory_root=tmp_path / "memory")

    with pytest.raises(InvalidWorkflowError):
        builder.build("alchemised", "invalid", "light")


def test_invalid_spoiler_level_raises(tmp_path: Path) -> None:
    builder = ContextBuilder(memory_root=tmp_path / "memory")

    with pytest.raises(InvalidSpoilerLevelError):
        builder.build("alchemised", "review", "invalid")


def test_missing_file_error_propagates(tmp_path: Path) -> None:
    builder = ContextBuilder(memory_root=tmp_path / "memory")

    with pytest.raises(MemoryFileNotFoundError):
        builder.build("alchemised", "review", "light")
