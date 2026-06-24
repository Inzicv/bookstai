"""Local search over Markdown book files."""

from __future__ import annotations

import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    title: str
    path: str
    score: int
    snippet: str


def extract_title(content: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


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
    """Indexes and searches markdown book files locally."""

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
            connection.execute("DELETE FROM books")

            count = 0
            for path in sorted(self.books_dir.glob("*.md")):
                content = path.read_text(encoding="utf-8")
                title = extract_title(content, path.stem)
                connection.execute(
                    "INSERT OR REPLACE INTO books (path, title, content) VALUES (?, ?, ?)",
                    (str(path.resolve()), title, content),
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
