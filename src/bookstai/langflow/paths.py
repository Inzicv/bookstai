"""Path resolution helpers for BookstAI Langflow adapters."""

from __future__ import annotations

from pathlib import Path

import bookstai


def resolve_bookstai_path(value: str | Path) -> Path:
    """Resolve a BookstAI path independently from the current working directory."""

    path = Path(value)

    if path.is_absolute():
        return path

    if path.exists():
        return path

    package_root = Path(bookstai.__file__).resolve().parent

    normalized = path
    if normalized.parts and normalized.parts[0] == "bookstai":
        normalized = Path(*normalized.parts[1:])

    candidates = [
        package_root / normalized,
        package_root.parent / normalized,
        package_root.parent.parent / normalized,
    ]

    if normalized.parts[:1] == ("prompts",):
        candidates.insert(0, package_root / normalized)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return package_root / normalized
