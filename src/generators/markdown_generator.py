"""Module for generating markdown files from BookMemory data."""

import os
import re

from src.models.book import BookMemory


def clean_filename(title: str) -> str:
    """Cleans a string to make it safe for use as a filename."""
    cleaned = re.sub(r'[\\/*?:"<>|]', "", title)
    cleaned = cleaned.strip().replace(" ", "_")
    return cleaned if cleaned else "unknown_book"


def generate_markdown(book: BookMemory, output_dir: str = "memory/books") -> str:
    """Generates a Markdown file representing the book's memory."""
    os.makedirs(output_dir, exist_ok=True)

    md_lines: list[str] = []
    md_lines.append(f"# {book.title}")
    md_lines.append(f"**Auteur :** {book.author}")
    md_lines.append("")

    md_lines.append("# Résumé")
    md_lines.append(book.summary)
    md_lines.append("")

    md_lines.append("# Descriptions physiques")
    if book.physical_descriptions:
        md_lines.extend(f"- {item}" for item in book.physical_descriptions)
    else:
        md_lines.append("*Aucune description physique répertoriée.*")
    md_lines.append("")

    md_lines.append("# Personnages")
    if book.characters:
        md_lines.extend(f"- {char}" for char in book.characters)
    else:
        md_lines.append("*Aucun personnage répertorié.*")
    md_lines.append("")

    md_lines.append("# Tropes")
    if book.tropes:
        md_lines.extend(f"- {trope}" for trope in book.tropes)
    else:
        md_lines.append("*Aucun trope répertorié.*")
    md_lines.append("")

    md_lines.append("# Thèmes")
    if book.themes:
        md_lines.extend(f"- {theme}" for theme in book.themes)
    else:
        md_lines.append("*Aucun thème répertorié.*")
    md_lines.append("")

    md_lines.append("# Timeline")
    if book.timeline:
        md_lines.extend(f"- {event}" for event in book.timeline)
    else:
        md_lines.append("*Aucun événement de timeline répertorié.*")
    md_lines.append("")

    md_lines.append("# Scènes importantes")
    if book.important_scenes:
        md_lines.extend(f"- {scene}" for scene in book.important_scenes)
    else:
        md_lines.append("*Aucune scène importante répertoriée.*")
    md_lines.append("")

    md_lines.append("# Citations")
    if book.quotes:
        md_lines.extend(f"> {quote}" for quote in book.quotes)
    else:
        md_lines.append("*Aucune citation répertoriée.*")
    md_lines.append("")

    content = "\n".join(md_lines)
    filename = f"{clean_filename(book.title)}.md"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return os.path.abspath(file_path)
