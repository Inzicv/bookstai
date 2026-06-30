"""Tests for Learning Loop draft application."""

from __future__ import annotations

from pathlib import Path

from bookstai.core.errors import LearningApplyError
from bookstai.learning import LearningDraftApplier


def test_applier_creates_memory_root(tmp_path) -> None:
    root = tmp_path / "memory"

    applier = LearningDraftApplier(memory_root=root)

    assert root.exists()
    assert root.is_dir()
    assert applier.memory_root == root


def test_apply_creates_memory_file_and_appends_block(tmp_path) -> None:
    draft_path = tmp_path / "draft.md"
    draft_path.write_text("# Draft body", encoding="utf-8")
    applier = LearningDraftApplier(memory_root=tmp_path / "memory")

    result = applier.apply(draft_path=draft_path, memory_file="books/book.md")

    assert result.applied is True
    assert result.draft_path == draft_path
    assert result.memory_path == (tmp_path / "memory" / "books" / "book.md").resolve()
    assert result.backup_path is None
    content = result.memory_path.read_text(encoding="utf-8")
    assert "Learning Update" in content
    assert "_Source draft:" in content
    assert "# Draft body" in content


def test_apply_creates_backup_when_memory_exists(tmp_path) -> None:
    draft_path = tmp_path / "draft.md"
    draft_path.write_text("# Draft body", encoding="utf-8")
    memory_root = tmp_path / "memory"
    memory_file = memory_root / "books" / "book.md"
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    memory_file.write_text("old memory", encoding="utf-8")
    applier = LearningDraftApplier(memory_root=memory_root)

    result = applier.apply(draft_path=draft_path, memory_file="books/book.md")

    assert result.backup_path is not None
    assert result.backup_path.exists()
    assert result.backup_path.read_text(encoding="utf-8") == "old memory"
    updated = memory_file.read_text(encoding="utf-8")
    assert updated.startswith("old memory\n\n---\n\n# Learning Update")


def test_apply_rejects_missing_draft(tmp_path) -> None:
    applier = LearningDraftApplier(memory_root=tmp_path / "memory")

    try:
        applier.apply(draft_path=tmp_path / "missing.md", memory_file="books/book.md")
        assert False, "LearningApplyError expected"
    except LearningApplyError as exc:
        assert str(exc) == "Learning draft file was not found."


def test_apply_rejects_dangerous_memory_file(tmp_path) -> None:
    draft_path = tmp_path / "draft.md"
    draft_path.write_text("# Draft", encoding="utf-8")
    applier = LearningDraftApplier(memory_root=tmp_path / "memory")

    for memory_file in ("../evil.md", "../../outside.md", "/tmp/evil.md"):
        try:
            applier.apply(draft_path=draft_path, memory_file=memory_file)
            assert False, "LearningApplyError expected"
        except LearningApplyError as exc:
            assert str(exc) == "Learning memory target is invalid."


def test_apply_rejects_absolute_path_outside_memory_root(tmp_path) -> None:
    draft_path = tmp_path / "draft.md"
    draft_path.write_text("# Draft", encoding="utf-8")
    applier = LearningDraftApplier(memory_root=tmp_path / "memory")
    outside = tmp_path / "outside.md"

    try:
        applier.apply(draft_path=draft_path, memory_file=outside)
        assert False, "LearningApplyError expected"
    except LearningApplyError as exc:
        assert str(exc) == "Learning memory target is invalid."


def test_apply_does_not_touch_real_memory_directory(tmp_path) -> None:
    draft_path = tmp_path / "draft.md"
    draft_path.write_text("# Draft body", encoding="utf-8")
    applier = LearningDraftApplier(memory_root=tmp_path / "memory")

    before = None
    real_memory = Path("memory")
    if real_memory.exists():
        before = sorted(str(path) for path in real_memory.rglob("*"))

    applier.apply(draft_path=draft_path, memory_file="books/book.md")

    after = None
    if real_memory.exists():
        after = sorted(str(path) for path in real_memory.rglob("*"))

    assert after == before
