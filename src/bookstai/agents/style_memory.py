"""Style memory agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..memory.reader import MemoryReader


class StyleMemoryAgent:
    """Load style-related memory files into a structured context."""

    def __init__(self, memory_root: Path) -> None:
        self.memory_root = Path(memory_root)
        self.reader = MemoryReader()

    def build(self) -> dict[str, Any]:
        context: dict[str, Any] = {}

        reviews_path = self.memory_root / "reviews" / "reviews.md"
        if reviews_path.exists():
            context["reviews"] = self.reader.read_sections(reviews_path)

        humor_path = self.memory_root / "humor" / "references.md"
        if humor_path.exists():
            context["humor"] = self.reader.read_sections(humor_path)

        songs_root = self.memory_root / "songs"
        if songs_root.exists():
            songs: dict[str, Any] = {}
            for song_path in sorted(songs_root.glob("*.md")):
                songs[song_path.stem] = self.reader.read_sections(song_path)
            if songs:
                context["songs"] = songs

        return context
