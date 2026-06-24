"""Module for generating markdown files from BookMemory data."""

import os
import re
from src.models.book import BookMemory


def clean_filename(title: str) -> str:
    """Cleans a string to make it safe for use as a filename.

    Args:
        title: The original book title.

    Returns:
        A sanitized filename string.
    """
    # Remove characters that are generally invalid in filenames
    cleaned = re.sub(r'[\\/*?:"<>|]', "", title)
    # Replace spaces with underscores
    cleaned = cleaned.strip().replace(" ", "_")
    return cleaned if cleaned else "unknown_book"


def generate_markdown(book: BookMemory, output_dir: str = "memory/books") -> str:
    """Generates a Markdown file representing the book's memory.

    Args:
        book: The BookMemory instance containing the extracted data.
        output_dir: The directory where the markdown file will be saved.

    Returns:
        The absolute path to the generated markdown file.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Format the content matching the requested sections
    md_lines = []
    md_lines.append(f"# {book.title}")
    md_lines.append(f"**Auteur :** {book.author}\n")

    md_lines.append("# Résumé")
    md_lines.append(f"{book.summary}\n")

    md_lines.append("# Personnages")
    if book.characters:
        for char in book.characters:
            md_lines.append(f"- {char}")
    else:
        md_lines.append("*Aucun personnage répertorié.*")
    md_lines.append("")

    md_lines.append("# Tropes")
    if book.tropes:
        for trope in book.tropes:
            md_lines.append(f"- {trope}")
    else:
        md_lines.append("*Aucun trope répertorié.*")
    md_lines.append("")

    md_lines.append("# Thèmes")
    if book.themes:
        for theme in book.themes:
            md_lines.append(f"- {theme}")
    else:
        md_lines.append("*Aucun thème répertorié.*")
    md_lines.append("")

    md_lines.append("# Citations")
    if book.quotes:
        for quote in book.quotes:
            # Format quotes as blockquotes
            md_lines.append(f"> {quote}")
    else:
        md_lines.append("*Aucune citation répertoriée.*")
    md_lines.append("")

    content = "\n".join(md_lines)

    filename = f"{clean_filename(book.title)}.md"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return os.path.abspath(file_path)
