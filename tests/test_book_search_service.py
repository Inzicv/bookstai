"""Tests for the local book search service."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.generators.markdown_generator import create_empty_book_template
from src.services.book_search_service import (
    BookSearchService,
    normalize_section_title,
    split_markdown_sections,
)


class TestBookSearchService(unittest.TestCase):
    def test_split_markdown_sections(self) -> None:
        content = """# Livre

### 1. Personnages

* Alice

### 2. Tropes

* enemies-to-lovers
"""
        sections = split_markdown_sections(content)
        self.assertGreaterEqual(len(sections), 2)
        self.assertTrue(any(section == "Personnages" for section, _, _ in sections))
        self.assertTrue(any(section == "Tropes" for section, _, _ in sections))
        self.assertTrue(any("enemies-to-lovers" in text for _, text, _ in sections))

    def test_normalize_section_title(self) -> None:
        self.assertEqual(normalize_section_title("Personnages (Nom, Prénom & Description physique)"), "Personnages")
        self.assertEqual(normalize_section_title("Timeline des Événements"), "Timeline")

    def test_index_and_section_hits(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            books_dir = Path(tmpdir) / "books"
            db_path = Path(tmpdir) / "book_index.sqlite"

            file_path = create_empty_book_template("Les Héritiers d'Orion", output_dir=str(books_dir))
            Path(file_path).write_text(
                "# Les Héritiers d'Orion\n\n### 2. Tropes Littéraires\n\n* enemies-to-lovers\n",
                encoding="utf-8",
            )

            service = BookSearchService(books_dir=str(books_dir), db_path=str(db_path))
            indexed = service.index_books()
            hits = service.extract_section_hits("enemies", file_path)
            memory_results = service.memory_search("enemies")

            self.assertEqual(indexed, 1)
            self.assertGreaterEqual(len(hits), 1)
            self.assertEqual(hits[0].section, "Tropes")
            self.assertIn("enemies-to-lovers", hits[0].content)
            self.assertEqual(len(memory_results), 1)


if __name__ == "__main__":
    unittest.main()
