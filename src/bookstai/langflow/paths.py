"""Path resolution helpers for BookstAI Langflow adapters."""

from __future__ import annotations

from pathlib import Path

import bookstai


def resolve_bookstai_path(value: str | Path, fallback_dir_name: str) -> Path:
    """Resolve a BookstAI path independently from the current working directory."""

    raw_path = Path(value).expanduser()

    if raw_path.is_absolute():
        return raw_path

    cwd_candidate = Path.cwd() / raw_path
    if cwd_candidate.exists():
        return cwd_candidate

    package_root = Path(bookstai.__file__).resolve().parent
    normalized = raw_path
    if normalized.parts and normalized.parts[0] == "bookstai":
        normalized = Path(*normalized.parts[1:])

    for parent in package_root.parents:
        candidate = parent / fallback_dir_name
        if candidate.exists():
            if normalized == Path(fallback_dir_name):
                return candidate
            nested_candidate = candidate / Path(*normalized.parts[1:]) if normalized.parts and normalized.parts[0] == fallback_dir_name else candidate / normalized
            if nested_candidate.exists():
                return nested_candidate

    project_root = package_root.parents[1]
    return project_root / normalized
