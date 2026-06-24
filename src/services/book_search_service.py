"""Local retrieval over Markdown book files."""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


SECTION_PATTERN = re.compile(r"^#{1,6}\s+(.+)$", flags=re.MULTILINE)

SECTION_ALIASES: dict[str, str] = {
    "personnages": "Personnages",
    "personnages principaux": "Personnages",
    "personnages (nom, prénom & description physique)": "Personnages",
    "tropes": "Tropes",
    "tropes littéraires": "Tropes",
    "résumé": "Résumé",
    "résumé du tome": "Résumé",
    "résumé spoiler-free": "Résumé spoiler-free",
    "citations": "Citations",
    "citations clés": "Citations",
    "timeline": "Timeline",
    "timeline des événements": "Timeline",
    "scènes importantes": "Scènes importantes",
    "relations entre personnages": "Relations entre personnages",
    "descriptions physiques": "Descriptions physiques",
    "thèmes": "Thèmes",
}


@dataclass
class SearchResult:
    title: str
    path: str
    score: int
    snippet: str


@dataclass
class SectionHit:
    title: str
    section: str
    content: str
    score: int
    path: str


@dataclass
class BookContext:
    title: str
    path: str
    sections: dict[str, str]

    def export_text(self) -> str:
        lines = [f"Title: {self.title}", f"Path: {self.path}", ""]
        for name, content in self.sections.items():
            lines.append(f"## {name}")
            lines.append(content)
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


def extract_title(content: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def split_markdown_sections(content: str) -> list[tuple[str, str, int]]:
    lines = content.splitlines()
    sections: list[tuple[str, list[str], int]] = []
    current_section = "Front matter"
    current_lines: list[str] = []
    order = 0
    seen_title = False

    def push_section() -> None:
        nonlocal order, current_lines
        sections.append((current_section, "\n".join(current_lines).strip(), order))
        order += 1
        current_lines = []

    for line in lines:
        match = SECTION_PATTERN.match(line)
        if match:
            if not seen_title and line.startswith("# "):
                seen_title = True
                continue
            if current_lines or not sections:
                push_section()
            current_section = normalize_section_title(match.group(1).strip())
        else:
            current_lines.append(line)

    push_section()
    return [(section, text, index) for section, text, index in sections if text]


def normalize_section_title(title: str) -> str:
    lowered = re.sub(r"^\d+[\s\.\-\)]*", "", title.lower().strip())
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return SECTION_ALIASES.get(lowered, title)


def build_snippet(content: str, query: str, width: int = 180) -> str:
    lowered = content.lower()
    needle = query.lower().strip()
    index = lowered.find(needle)
    if index < 0:
        return content[:width].replace("\n", " ").strip()
    start = max(0, index - width // 2)
    end = min(len(content), index + len(query) + width // 2)
    return content[start:end].replace("\n", " ").strip()


class BookSearchService:
    """Indexes and retrieves markdown book files locally."""

    def __init__(self, books_dir: str = "memory/books", db_path: str = "memory/book_index.sqlite") -> None:
        self.books_dir = Path(books_dir)
        self.db_path = Path(db_path)

    def index_books(self) -> int:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    path TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_path TEXT NOT NULL,
                    title TEXT NOT NULL,
                    section TEXT NOT NULL,
                    content TEXT NOT NULL,
                    section_order INTEGER NOT NULL
                )
                """
            )
            connection.execute("DELETE FROM books")
            connection.execute("DELETE FROM chunks")

            count = 0
            for path in sorted(self.books_dir.glob("*.md")):
                content = path.read_text(encoding="utf-8")
                title = extract_title(content, path.stem)
                connection.execute(
                    "INSERT OR REPLACE INTO books (path, title, content) VALUES (?, ?, ?)",
                    (str(path.resolve()), title, content),
                )

                for section, section_content, section_order in split_markdown_sections(content):
                    connection.execute(
                        """
                        INSERT INTO chunks (book_path, title, section, content, section_order)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (str(path.resolve()), title, section, section_content, section_order),
                    )

                count += 1

            connection.commit()
            return count
        finally:
            connection.close()

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        if not query.strip():
            return []

        if not self.db_path.exists():
            self.index_books()

        connection = sqlite3.connect(self.db_path)
        try:
            rows = connection.execute("SELECT title, path, content FROM books").fetchall()
        finally:
            connection.close()

        scored: list[SearchResult] = []
        terms = [term.lower() for term in re.findall(r"\w+", query)]
        for title, path, content in rows:
            haystack = f"{title}\n{content}".lower()
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                scored.append(
                    SearchResult(
                        title=title,
                        path=path,
                        score=score,
                        snippet=build_snippet(content, query),
                    )
                )

        scored.sort(key=lambda item: (-item.score, item.title.lower()))
        return scored[:limit]

    def extract_section_hits(self, query: str, path: str, limit: int = 3) -> list[SectionHit]:
        if not self.db_path.exists():
            self.index_books()

        connection = sqlite3.connect(self.db_path)
        try:
            rows = connection.execute(
                "SELECT title, section, content, section_order FROM chunks WHERE book_path = ?",
                (path,),
            ).fetchall()
        finally:
            connection.close()

        terms = [term.lower() for term in re.findall(r"\w+", query)]
        hits: list[SectionHit] = []
        for title, section, content, _section_order in rows:
            haystack = content.lower()
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                hits.append(
                    SectionHit(
                        title=title,
                        section=section,
                        content=content[:500].strip(),
                        score=score,
                        path=path,
                    )
                )

        hits.sort(key=lambda item: (-item.score, item.section.lower()))
        return hits[:limit]

    def memory_search(self, query: str, limit: int = 5) -> list[tuple[SearchResult, list[SectionHit]]]:
        results = self.search(query, limit=limit)
        return [(result, self.extract_section_hits(query, result.path)) for result in results]

    def load_book_context(self, path: str) -> BookContext:
        content = Path(path).read_text(encoding="utf-8")
        title = extract_title(content, Path(path).stem)
        sections: dict[str, str] = {}
        for section, section_content, _order in split_markdown_sections(content):
            if section == title:
                continue
            sections[section] = section_content
        return BookContext(title=title, path=str(Path(path).resolve()), sections=sections)

    def export_context(self, path: str, output_path: str | None = None) -> str:
        context = self.load_book_context(path)
        destination = Path(output_path) if output_path else Path(path).with_suffix(".context.txt")
        destination.write_text(context.export_text(), encoding="utf-8")
        return str(destination.resolve())
