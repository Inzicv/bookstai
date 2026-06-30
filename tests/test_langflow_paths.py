"""Tests for Langflow path resolution."""

from __future__ import annotations

from pathlib import Path

import bookstai

from bookstai.langflow.paths import resolve_bookstai_path


def test_resolve_bookstai_path_keeps_absolute_path(tmp_path: Path) -> None:
    absolute = tmp_path / "absolute"

    assert resolve_bookstai_path(absolute) == absolute


def test_resolve_bookstai_path_keeps_existing_relative_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    relative = Path("existing")
    relative.mkdir()

    assert resolve_bookstai_path(relative) == relative


def test_resolve_bookstai_path_prefers_package_prompts_when_missing_elsewhere(
    monkeypatch,
    tmp_path: Path,
) -> None:
    package_root = tmp_path / "site-packages" / "bookstai"
    prompts_dir = package_root / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    fake_init = package_root / "__init__.py"
    fake_init.write_text("__all__ = []", encoding="utf-8")
    monkeypatch.setattr(bookstai, "__file__", str(fake_init))

    monkeypatch.chdir(tmp_path)

    assert resolve_bookstai_path("prompts") == prompts_dir
