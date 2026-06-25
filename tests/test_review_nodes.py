"""Tests for Langflow-friendly review nodes."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.langflow.review_nodes import (
    assemble_review_script,
    generate_avis,
    generate_hooks,
    generate_pitch,
    load_review_context,
)


class TestReviewNodes(unittest.TestCase):
    def test_nodes_return_simple_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            books_dir = Path(tmpdir) / "memory" / "books"
            books_dir.mkdir(parents=True, exist_ok=True)
            book_path = books_dir / "lesheritiersdorion.md"
            book_path.write_text(
                "# Les Héritiers d'Orion\n\n## Résumé\n\nUn empire en guerre.\n\n## Tropes\n\n* enemies-to-lovers\n\n## Scènes importantes\n\n* duel final\n",
                encoding="utf-8",
            )

            reviews_dir = Path(tmpdir) / "memory" / "reviews"
            reviews_dir.mkdir(parents=True, exist_ok=True)
            (reviews_dir / "reviews.md").write_text(
                "#pitch\nUne vieille review pitch.\n#avis\nUn vieil avis.\n",
                encoding="utf-8",
            )

            humor_dir = Path(tmpdir) / "memory" / "humor"
            humor_dir.mkdir(parents=True, exist_ok=True)
            (humor_dir / "references.md").write_text(
                "Roman Frayssinet\nMister V\nFreddy Gladieux\n",
                encoding="utf-8",
            )

            context = load_review_context("lesheritiersdorion")
            pitch = generate_pitch("lesheritiersdorion")
            avis = generate_avis("J'ai aimé la tension.", "Pitch validé", "lesheritiersdorion")
            hooks = generate_hooks("Pitch validé", "Avis validé", "lesheritiersdorion")
            script = assemble_review_script("Hook final", "Pitch validé", "Avis validé", "lesheritiersdorion")

            self.assertEqual(context["book_title"], "Les Héritiers d'Orion")
            self.assertIn("Proposition de pitch", pitch["title"])
            self.assertIn("Proposition d'avis", avis["title"])
            self.assertTrue(hooks["options"])
            self.assertIn("Script final", script["title"])
            self.assertIn("Hook final", script["content"])


if __name__ == "__main__":
    unittest.main()
