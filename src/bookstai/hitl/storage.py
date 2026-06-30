"""Persistence helpers for Human In The Loop sessions."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from ..core.errors import HITLSessionStorageError
from .session import HITLSession


class HITLSessionStorage:
    def __init__(self, root: str | Path = "outputs/hitl") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, session: HITLSession) -> Path:
        try:
            output_path = self._path_for(session.workflow_name, session.item_slug)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(session.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return output_path
        except OSError as exc:
            raise HITLSessionStorageError("Could not save HITL session.") from exc

    def load(self, path: str | Path) -> HITLSession:
        session_path = Path(path)
        try:
            raw = session_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise HITLSessionStorageError("HITL session file was not found.") from exc
        except OSError as exc:
            raise HITLSessionStorageError("Could not load HITL session.") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise HITLSessionStorageError("HITL session file is invalid JSON.") from exc

        self._validate_payload(data)

        try:
            return HITLSession.from_dict(data)
        except (KeyError, TypeError, ValueError) as exc:
            raise HITLSessionStorageError("HITL session data is invalid.") from exc

    def _path_for(self, workflow_name: str, item_slug: str) -> Path:
        return self.root / self._slugify(workflow_name) / f"{self._slugify(item_slug)}.json"

    def _validate_payload(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise HITLSessionStorageError("HITL session data is invalid.")

        required_keys = {"workflow_name", "item_slug", "steps"}
        if not required_keys.issubset(data):
            raise HITLSessionStorageError("HITL session data is invalid.")

        steps = data["steps"]
        if not isinstance(steps, list):
            raise HITLSessionStorageError("HITL session data is invalid.")

        for step in steps:
            if not isinstance(step, dict):
                raise HITLSessionStorageError("HITL session data is invalid.")
            for key in ("name", "status", "content"):
                if key not in step:
                    raise HITLSessionStorageError("HITL session data is invalid.")

    def _slugify(self, value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        normalized = normalized.lower()
        normalized = re.sub(r"[^a-z0-9]+", "", normalized)
        return normalized or "session"
