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
            assets = assistant.load_assets()
            pitch_step = assistant.propose_pitch_step(assets)
            avis_step = assistant.propose_avis_step(assets, "J'ai aimé la tension.")
            hooks_step = assistant.propose_hooks_step(assets)
            assemble_step = assistant.assemble_script_step(
                assets=assets,
                pitch_final=pitch_step.content,
                avis_final=avis_step.content,
                hook_final=hooks_step.options[0],
                user_notes="J'ai aimé la tension.",
            )

            self.assertEqual(assets.book_title, "Les Héritiers d'Orion")
            self.assertIn("pitch", pitch_step.step_name)
            self.assertIn("avis", avis_step.step_name)
            self.assertTrue(hooks_step.options)
            self.assertIn("## Accroche", assemble_step.content)
            self.assertIn("J'ai aimé la tension.", assemble_step.content)
            self.assertIn("Une vieille review pitch.", assemble_step.content)
            self.assertIn("Un vieil avis.", assemble_step.content)
            self.assertIn("Roman Frayssinet", assemble_step.content)


if __name__ == "__main__":
    unittest.main()
