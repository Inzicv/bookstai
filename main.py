"""Main CLI entrypoint for the local Librarian V1 book-sheet generator."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.generators.markdown_generator import clean_filename


@dataclass
class BookSheet:
    title: str = ""
    author: str = ""
    saga: str = ""
    tome: str = ""
    genre: str = ""
    spoiler_free_summary: str = ""
    full_summary: str = ""
    main_characters: list[str] = field(default_factory=list)
    physical_descriptions: list[str] = field(default_factory=list)
    relationships: list[str] = field(default_factory=list)
    tropes: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    key_quotes: list[str] = field(default_factory=list)
    important_scenes: list[str] = field(default_factory=list)
    timeline: list[str] = field(default_factory=list)
    personal_notes: str = ""
    reading_status: str = ""
    spoil_level: str = ""


def ask_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def ask_multiline(label: str) -> str:
    print(f"{label} (colle une zone de texte, termine par une ligne vide) :")
    lines: list[str] = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines).strip()


def ask_list(label: str) -> list[str]:
    raw = ask_multiline(label)
    if not raw:
        return []
    items = []
    for line in raw.splitlines():
        cleaned = re.sub(r"^[\-*•\d\.\)\s]+", "", line).strip()
        if cleaned:
            items.append(cleaned)
    if len(items) <= 1 and "\n" not in raw and ";" in raw:
        return [part.strip() for part in raw.split(";") if part.strip()]
    return items or [raw.strip()]


def collect_book_sheet() -> BookSheet:
    print("Mode fiche livre : entre les informations au fil des questions.\n")
    return BookSheet(
        title=ask_text("Titre"),
        author=ask_text("Auteur"),
        saga=ask_text("Saga"),
        tome=ask_text("Tome"),
        genre=ask_text("Genre"),
        spoiler_free_summary=ask_multiline("Résumé spoiler-free"),
        full_summary=ask_multiline("Résumé complet"),
        main_characters=ask_list("Personnages principaux"),
        physical_descriptions=ask_list("Descriptions physiques"),
        relationships=ask_list("Relations entre personnages"),
        tropes=ask_list("Tropes"),
        themes=ask_list("Thèmes"),
        key_quotes=ask_list("Citations clés"),
        important_scenes=ask_list("Scènes importantes"),
        timeline=ask_list("Timeline"),
        personal_notes=ask_multiline("Notes personnelles"),
        reading_status=ask_text("Statut de lecture"),
        spoil_level=ask_text("Niveau de spoil"),
    )


def render_list_section(title: str, items: list[str], fallback: str) -> list[str]:
    lines = [title, ""]
    if items:
        lines.extend(f"* {item}" for item in items)
    else:
        lines.append(fallback)
    lines.append("")
    return lines


def render_quote_section(items: list[str], fallback: str) -> list[str]:
    lines = ["# Citations clés", ""]
    if items:
        lines.extend(f"> {item}" if not item.startswith(">") else item for item in items)
    else:
        lines.append(fallback)
    lines.append("")
    return lines


def generate_book_markdown(book: BookSheet, output_dir: str = "memory/books") -> str:
    os.makedirs(output_dir, exist_ok=True)
    slug = clean_filename(book.title)
    file_path = Path(output_dir) / f"{slug}.md"

    lines: list[str] = []
    lines.append(f"# {book.title or 'Titre à compléter'}")
    lines.append("")
    lines.append(f"**Auteur :** {book.author or 'À compléter'}")
    lines.append(f"**Saga :** {book.saga or 'À compléter'}")
    lines.append(f"**Tome :** {book.tome or 'À compléter'}")
    lines.append(f"**Genre :** {book.genre or 'À compléter'}")
    lines.append(f"**Statut de lecture :** {book.reading_status or 'À compléter'}")
    lines.append(f"**Niveau de spoil :** {book.spoil_level or 'À compléter'}")
    lines.append("")

    lines.extend(["# Résumé spoiler-free", "", book.spoiler_free_summary or ""])
    lines.append("")
    lines.extend(["# Résumé complet", "", book.full_summary or ""])
    lines.append("")

    lines.extend(render_list_section("# Personnages principaux", book.main_characters, "*À compléter*"))
    lines.extend(render_list_section("# Descriptions physiques", book.physical_descriptions, "*À compléter*"))
    lines.extend(render_list_section("# Relations entre personnages", book.relationships, "*À compléter*"))
    lines.extend(render_list_section("# Tropes", book.tropes, "*À compléter*"))
    lines.extend(render_list_section("# Thèmes", book.themes, "*À compléter*"))
    lines.extend(render_quote_section(book.key_quotes, "*À compléter*"))
    lines.extend(render_list_section("# Scènes importantes", book.important_scenes, "*À compléter*"))
    lines.extend(render_list_section("# Timeline", book.timeline, "*À compléter*"))

    lines.extend(["# Notes personnelles", "", book.personal_notes or "*À compléter*", ""])

    file_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return str(file_path.resolve())


def generate_empty_template(title: str, output_dir: str = "memory/books") -> str:
    os.makedirs(output_dir, exist_ok=True)
    slug = clean_filename(title)
    file_path = Path(output_dir) / f"{slug}.md"

    template = """# {title}

**Auteur :** À compléter
**Saga :** À compléter
**Tome :** À compléter
**Genre :** À compléter
**Statut de lecture :** À compléter
**Niveau de spoil :** À compléter

# Résumé spoiler-free

À compléter

# Résumé complet

À compléter

# Personnages principaux

* À compléter

# Descriptions physiques

* À compléter

# Relations entre personnages

* À compléter

# Tropes

* À compléter

# Thèmes

* À compléter

# Citations clés

* À compléter

# Scènes importantes

* À compléter

# Timeline

* À compléter

# Notes personnelles

À compléter
""".format(title=title or "Titre à compléter")

    file_path.write_text(template, encoding="utf-8")
    return str(file_path.resolve())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="BookstAI Librarian V1 - Générateur local de fiches livres Markdown."
    )
    parser.add_argument(
        "--output-dir",
        default="memory/books",
        help="Répertoire de sortie pour le fichier Markdown.",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Crée un template vide à remplir manuellement.",
    )
    parser.add_argument(
        "--title",
        help="Titre utilisé pour le nom de fichier et le template vide.",
    )

    args = parser.parse_args()

    try:
        if args.template:
            title = args.title or ask_text("Titre du livre pour nommer le fichier")
            output_path = generate_empty_template(title, output_dir=args.output_dir)
        else:
            book = collect_book_sheet()
            output_path = generate_book_markdown(book, output_dir=args.output_dir)

        print(f"\n[Succès] Fiche générée : {output_path}")
    except KeyboardInterrupt:
        print("\n[Annulé] Génération interrompue par l'utilisateur.", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"\n[Erreur] La génération a échoué : {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
