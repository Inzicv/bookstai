"""Path resolution helpers for BookstAI Langflow adapters."""

from __future__ import annotations

from pathlib import Path

import bookstai


def resolve_bookstai_path(
    value: str | Path,
    fallback_dir_name: str | None = None,
) -> Path:
    """Resolve a BookstAI path independently from the current working directory."""

    raw_path = Path(value).expanduser()

    if raw_path.is_absolute():
        return raw_path

    cwd_candidate = Path.cwd() / raw_path
    if cwd_candidate.exists():
        return raw_path

    package_root = Path(bookstai.__file__).resolve().parent
    normalized = raw_path
    if normalized.parts and normalized.parts[0] == "bookstai":
        normalized = Path(*normalized.parts[1:])

    inferred_fallback = fallback_dir_name
    if inferred_fallback is None:
        inferred_fallback = normalized.parts[0] if normalized.parts else raw_path.name
        if inferred_fallback not in {"prompts", "memory"}:
            inferred_fallback = normalized.parts[0] if normalized.parts else raw_path.name

    if normalized == Path(inferred_fallback):
        search_target = Path(inferred_fallback)
    else:
        search_target = normalized

    for parent in package_root.parents:
        candidate = parent / inferred_fallback
        if candidate.exists():
            if search_target == Path(inferred_fallback):
                return candidate
            nested_candidate = candidate / Path(*search_target.parts[1:]) if search_target.parts and search_target.parts[0] == inferred_fallback else candidate / search_target
            if nested_candidate.exists():
                return nested_candidate

    return raw_path
