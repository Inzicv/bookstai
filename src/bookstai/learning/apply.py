"""Apply Learning Drafts into BookstAI memory."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ..core.errors import LearningApplyError


@dataclass
class LearningApplyResult:
    draft_path: Path
    memory_path: Path
    backup_path: Path | None
    applied: bool


class LearningDraftApplier:
    def __init__(self, memory_root: str | Path = "memory") -> None:
        self.memory_root = Path(memory_root)
        self.memory_root.mkdir(parents=True, exist_ok=True)

    def apply(self, draft_path: str | Path, memory_file: str | Path) -> LearningApplyResult:
        draft_path = Path(draft_path)
        if not draft_path.exists():
            raise LearningApplyError("Learning draft file was not found.")

        try:
            draft_text = draft_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise LearningApplyError("Could not apply learning draft.") from exc

        memory_path = self._resolve_memory_path(memory_file)
        memory_path.parent.mkdir(parents=True, exist_ok=True)

        backup_path = None
        if memory_path.exists():
            backup_path = self._create_backup(memory_path)
            try:
                existing_text = memory_path.read_text(encoding="utf-8")
            except OSError as exc:
                raise LearningApplyError("Could not apply learning draft.") from exc
            new_text = f"{existing_text}\n\n---\n\n# Learning Update\n\n_Source draft: {draft_path}_\n\n{draft_text}"
        else:
            new_text = f"---\n\n# Learning Update\n\n_Source draft: {draft_path}_\n\n{draft_text}"

        try:
            memory_path.write_text(new_text, encoding="utf-8")
        except OSError as exc:
            raise LearningApplyError("Could not apply learning draft.") from exc

        return LearningApplyResult(
            draft_path=draft_path,
            memory_path=memory_path,
            backup_path=backup_path,
            applied=True,
        )

    def _resolve_memory_path(self, memory_file: str | Path) -> Path:
        candidate = Path(memory_file)
        if candidate.is_absolute():
            resolved = candidate.resolve()
            try:
                resolved.relative_to(self.memory_root.resolve())
            except ValueError as exc:
                raise LearningApplyError("Learning memory target is invalid.") from exc
            return resolved

        normalized = Path(*candidate.parts)
        resolved = (self.memory_root / normalized).resolve()
        try:
            resolved.relative_to(self.memory_root.resolve())
        except ValueError as exc:
            raise LearningApplyError("Learning memory target is invalid.") from exc
        return resolved

    def _create_backup(self, memory_path: Path) -> Path:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        backup_path = Path(f"{memory_path}.bak.{timestamp}")
        backup_path.write_text(memory_path.read_text(encoding="utf-8"), encoding="utf-8")
        return backup_path
