"""Visual style reader for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..memory.reader import MemoryReader


class VisualStyleReader:
    """List and read manual visual style prompts from memory."""

    def __init__(self, memory_root: Path) -> None:
        self.styles_root = Path(memory_root) / "visual_style" / "Prompts_visuels"
        self.reader = MemoryReader()

    def list_styles(self) -> list[dict[str, Any]]:
        if not self.styles_root.exists():
            return []

        styles: list[dict[str, Any]] = []
        for style_path in sorted(self.styles_root.glob("*.md")):
            styles.append(self.read_style(style_path.stem))
        return styles

    def read_style(self, style_id: str) -> dict[str, Any]:
        style_path = self._resolve_style_path(style_id)
        instructions = self.reader.read_text(style_path)
        sections = self.reader.read_sections(style_path)
        return {
            "id": style_path.stem,
            "name": self._style_name(style_path.stem, sections),
            "source_path": style_path.as_posix(),
            "instructions": instructions,
            "sections": sections,
        }

    def _resolve_style_path(self, style_id: str) -> Path:
        candidates = [
            self.styles_root / f"{style_id}.md",
            self.styles_root / f"{style_id.replace(' ', '_')}.md",
        ]
        normalized = style_id.strip().lower().replace(" ", "_")
        for style_path in self.styles_root.glob("*.md"):
            if style_path.stem.lower() == normalized:
                candidates.append(style_path)
                break
        for candidate in candidates:
            if candidate.exists():
                return candidate
        raise FileNotFoundError(f"Visual style not found: {style_id}")

    def _style_name(self, style_id: str, sections: dict[str, str]) -> str:
        for key in ("title", "Titre", "name", "Nom"):
            value = sections.get(key)
            if value:
                first_line = value.strip().splitlines()[0].strip()
                if first_line:
                    return first_line.lstrip("# ").strip()
        return style_id.replace("_", " ").replace("-", " ").title()
