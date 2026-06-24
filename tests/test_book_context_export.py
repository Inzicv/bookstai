"""Tests for single-book context export."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.generators.markdown_generator import create_empty_book_template
from src.services.book_search_service import BookSearchService


class TestBookContextExport(unittest.TestCase):
    def test_load_and_export_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            books_dir = Path(tmpdir) / "books"
            source_path = create_empty_book_template("Les Héritiers d'Orion", output_dir=str(books_dir))
            Path(source_path).write_text(
                "# Les Héritiers d'Orion\n\n### 1. Personnages\n\n* Mads\n\n### 2. Tropes\n\n* enemies-to-lovers\n",
                encoding="utf-8",
            )

            service = BookSearchService(books_dir=str(books_dir))
            context = service.load_book_context(source_path)
            exported = service.export_context(source_path, output_path=str(Path(tmpdir) / "context.txt"))

            self.assertEqual(context.title, "Les Héritiers d'Orion")
            self.assertIn("Personnages", context.sections)
            self.assertIn("Tropes", context.sections)
            self.assertTrue(Path(exported).exists())
            self.assertIn("## Personnages", Path(exported).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
