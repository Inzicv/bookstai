"""Tests for the local book-sheet generator."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import main


class TestLocalGenerator(unittest.TestCase):
    def test_generate_book_markdown(self) -> None:
        book = main.BookSheet(
            title="Le Petit Prince",
            author="Antoine de Saint-Exupéry",
            saga="",
            tome="1",
            genre="Conte philosophique",
            spoiler_free_summary="Un pilote rencontre un petit prince venu d'une autre planète.",
            full_summary="Résumé complet ici.",
            main_characters=["Le Petit Prince", "L'aviateur"],
            physical_descriptions=["Petit garçon blond avec une écharpe."],
            relationships=["Le Petit Prince et le renard"],
            tropes=["Voyage initiatique"],
            themes=["Amitié", "Deuil"],
            key_quotes=["On ne voit bien qu'avec le cœur."],
            important_scenes=["La rencontre avec le renard"],
            timeline=["Rencontre avec l'aviateur"],
            personal_notes="Notes perso.",
            reading_status="Lu",
            spoil_level="Complet",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = main.generate_book_markdown(book, output_dir=tmpdir)
            content = Path(path).read_text(encoding="utf-8")

            self.assertIn("# Le Petit Prince", content)
            self.assertIn("**Auteur :** Antoine de Saint-Exupéry", content)
            self.assertIn("# Résumé spoiler-free", content)
            self.assertIn("Le Petit Prince et le renard", content)
            self.assertIn("> On ne voit bien qu'avec le cœur.", content)

    def test_generate_empty_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = main.generate_empty_template("Livre Test", output_dir=tmpdir)
            content = Path(path).read_text(encoding="utf-8")

            self.assertIn("# Livre Test", content)
            self.assertIn("À compléter", content)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
