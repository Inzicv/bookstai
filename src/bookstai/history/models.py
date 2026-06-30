"""Execution history models for BookstAI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class HistoryEntry:
    command: str
    status: str
    workflow_name: str | None = None
    item_slug: str | None = None
    hitl_enabled: bool = False
    provider: str | None = None
    image_backend: str | None = None
    artifacts: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "status": self.status,
            "workflow_name": self.workflow_name,
            "item_slug": self.item_slug,
            "hitl_enabled": self.hitl_enabled,
            "provider": self.provider,
            "image_backend": self.image_backend,
            "artifacts": self._normalize(self.artifacts),
            "error": self.error,
            "created_at": self.created_at,
        }

    def _normalize(self, value: Any) -> Any:
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, dict):
            return {key: self._normalize(inner) for key, inner in value.items()}
        if isinstance(value, list):
            return [self._normalize(inner) for inner in value]
        if isinstance(value, tuple):
            return [self._normalize(inner) for inner in value]
        return value
