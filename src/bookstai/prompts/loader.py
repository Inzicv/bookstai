"""Prompt loader for BookstAI."""

from __future__ import annotations

from pathlib import Path

from ..core.errors import EmptyPromptFileError, PromptFileNotFoundError


class PromptLoader:
    """Load raw Markdown prompt templates from disk."""

    def __init__(self, prompt_root: Path) -> None:
        self.prompt_root = Path(prompt_root)

    def load(self, prompt_path: str | Path) -> str:
        file_path = self.prompt_root / Path(prompt_path)
        self._validate_file(file_path)
        return file_path.read_text(encoding="utf-8")

    def _validate_file(self, file_path: Path) -> None:
        if not file_path.exists():
            raise PromptFileNotFoundError(f"Prompt file not found: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        if not content.strip():
            raise EmptyPromptFileError(f"Prompt file is empty: {file_path}")
