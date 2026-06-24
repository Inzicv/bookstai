"""Tests for the Review Assistant service."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.services.review_assistant_service import ReviewAssistantService


class TestReviewAssistantService(unittest.TestCase):
    def test_build_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            book_path = Path(tmpdir) / "book.md"
            reviews_path = Path(tmpdir) / "reviews.md"
            humor_path = Path(tmpdir) / "humor.md"

            book_path.write_text(
                "# Les Héritiers d'Orion\n\n## Résumé\n\nUn empire en guerre.\n\n## Tropes\n\n* enemies-to-lovers\n\n## Scènes importantes\n\n* duel final\n",
                encoding="utf-8",
            )
            reviews_path.write_text("#pitch\nUne vieille review pitch.\n#avis\nUn vieil avis.\n", encoding="utf-8")
            humor_path.write_text("Roman Frayssinet\nMister V\nFreddy Gladieux\n", encoding="utf-8")

            assistant = ReviewAssistantService(
                book_path=str(book_path),
                reviews_path=str(reviews_path),
                humor_path=str(humor_path),
            )
            draft = assistant.build_draft(user_notes="J'ai aimé la tension.")

            self.assertEqual(draft.book_title, "book")
            self.assertTrue(draft.hook_suggestions)
            self.assertIn("Hook", draft.final_script)
            self.assertIn("J'ai aimé la tension.", draft.final_script)
            self.assertIn("Une vieille review pitch.", draft.final_script)


if __name__ == "__main__":
    unittest.main()
