"""Tests for the local book search service."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.generators.markdown_generator import create_empty_book_template
from src.services.book_search_service import BookSearchService


class TestBookSearchService(unittest.TestCase):
    def test_index_and_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            books_dir = Path(tmpdir) / "books"
            db_path = Path(tmpdir) / "book_index.sqlite"

            file_path = create_empty_book_template("Les Héritiers d'Orion", output_dir=str(books_dir))
            Path(file_path).write_text(
                "# Les Héritiers d'Orion\n\n# Tropes\n\n* enemies-to-lovers\n",
                encoding="utf-8",
            )

            service = BookSearchService(books_dir=str(books_dir), db_path=str(db_path))
            indexed = service.index_books()
            results = service.search("enemies")

            self.assertEqual(indexed, 1)
            self.assertEqual(len(results), 1)
            self.assertIn("Les Héritiers d'Orion", results[0].title)
            self.assertIn("enemies-to-lovers", results[0].snippet)


if __name__ == "__main__":
    unittest.main()
