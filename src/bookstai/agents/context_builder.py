"""Context builder agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..memory.reader import MemoryReader


class ContextBuilder:
    """Build a raw context from a book memory file."""

    def __init__(self, memory_root: Path) -> None:
        self.memory_root = Path(memory_root)
        self.reader = MemoryReader()

    def build(
        self,
        book_slug: str,
        workflow_type: str,
        spoiler_level: str,
    ) -> dict[str, Any]:
        source_path = self.memory_root / "books" / f"{book_slug}.md"
        sections = self.reader.read_sections(source_path)

        return {
            "book_slug": book_slug,
            "workflow_type": workflow_type,
            "spoiler_level": spoiler_level,
            "source_path": str(source_path),
            "sections": sections,
            "warnings": [],
        }
