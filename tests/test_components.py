"""Unit tests for the BookstAI components."""

import os
import unittest
from src.models.book import BookMemory
from src.generators.markdown_generator import clean_filename, generate_markdown


class TestMarkdownGenerator(unittest.TestCase):
    """Test cases for clean_filename and generate_markdown functions."""

    def test_clean_filename(self) -> None:
        self.assertEqual(clean_filename("Hello World"), "Hello_World")
        self.assertEqual(clean_filename("Test/With:Invalid?Chars"), "TestWithInvalidChars")
        self.assertEqual(clean_filename("   Spaces   "), "Spaces")

    def test_generate_markdown(self) -> None:
        book = BookMemory(
            title="Le Petit Prince",
            author="Antoine de Saint-Exupéry",
            summary="Un petit garçon voyage à travers les planètes.",
            characters=["Le Petit Prince", "L'aviateur", "La Rose", "Le Renard"],
            tropes=["Voyage initiatique", "Allégorie"],
            themes=["Amitié", "Amour", "Perte", "Adulte vs Enfant"],
            quotes=["On ne voit bien qu'avec le cœur. L'essentiel est invisible pour les yeux."]
        )
        
        output_dir = "memory/test_books"
        file_path = generate_markdown(book, output_dir=output_dir)
        
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("# Le Petit Prince", content)
        self.assertIn("Antoine de Saint-Exupéry", content)
        self.assertIn("# Résumé", content)
        self.assertIn("Un petit garçon voyage", content)
        self.assertIn("- Le Petit Prince", content)
        self.assertIn("- Voyage initiatique", content)
        self.assertIn("> On ne voit bien qu'avec le cœur.", content)
        
        # Cleanup
        os.remove(file_path)
        os.rmdir(output_dir)


if __name__ == "__main__":
    unittest.main()
