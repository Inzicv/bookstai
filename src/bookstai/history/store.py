"""JSONL execution history store for BookstAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core.errors import BookstAIError
from .models import HistoryEntry


class HistoryStoreError(BookstAIError):
    """Raised when execution history cannot be read or written."""


class HistoryStore:
    def __init__(self, path: str | Path = "outputs/history/bookstai-history.jsonl") -> None:
        self.path = Path(path)

    def append(self, entry: HistoryEntry) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
        return self.path

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        entries: list[dict[str, Any]] = []
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise HistoryStoreError("History file is invalid JSONL.") from exc
        return entries

    def tail(self, limit: int = 10) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        entries = self.read_all()
        return entries[-limit:]
