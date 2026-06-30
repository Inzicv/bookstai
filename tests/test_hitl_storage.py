"""Tests for HITL session storage."""

from __future__ import annotations

import json

from bookstai.core.errors import HITLSessionStorageError
from bookstai.hitl import HITLSession, HITLSessionStorage


def test_storage_creates_root_directory(tmp_path) -> None:
    root = tmp_path / "hitl"

    storage = HITLSessionStorage(root=root)

    assert root.exists()
    assert root.is_dir()
    assert storage.root == root


def test_save_writes_json_and_returns_path(tmp_path) -> None:
    storage = HITLSessionStorage(root=tmp_path / "hitl")
    session = HITLSession(workflow_name="review", item_slug="lesheritiersdorion")
    session.add_step(name="comedy", content={"response": "ok"}, metadata={"source": "llm"})

    path = storage.save(session)

    assert path.exists()
    assert path.name == "lesheritiersdorion.json"
    assert path.parent.name == "review"

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["workflow_name"] == "review"
    assert data["item_slug"] == "lesheritiersdorion"
    assert data["steps"]


def test_load_reconstructs_session_round_trip(tmp_path) -> None:
    storage = HITLSessionStorage(root=tmp_path / "hitl")
    session = HITLSession(workflow_name="song", item_slug="lesheritiersdorion")
    session.add_step(
        name="song",
        content={"response": "original"},
        metadata={"source": "llm"},
    )
    session.approve_step("song", comment="OK")
    session.edit_step("song", edited_content={"response": "edited"}, comment="Corrige")

    path = storage.save(session)
    loaded = storage.load(path)

    assert loaded.workflow_name == "song"
    assert loaded.item_slug == "lesheritiersdorion"
    step = loaded.get_step("song")
    assert step.name == "song"
    assert step.status.value == "edited"
    assert step.content == {"response": "original"}
    assert step.edited_content == {"response": "edited"}
    assert step.comment == "Corrige"
    assert step.metadata == {"source": "llm"}


def test_load_missing_file_raises_storage_error(tmp_path) -> None:
    storage = HITLSessionStorage(root=tmp_path / "hitl")
    path = tmp_path / "missing.json"

    try:
        storage.load(path)
        assert False, "HITLSessionStorageError expected"
    except HITLSessionStorageError as exc:
        assert str(exc) == "HITL session file was not found."


def test_load_invalid_json_raises_storage_error(tmp_path) -> None:
    storage = HITLSessionStorage(root=tmp_path / "hitl")
    path = tmp_path / "invalid.json"
    path.write_text("{not json}", encoding="utf-8")

    try:
        storage.load(path)
        assert False, "HITLSessionStorageError expected"
    except HITLSessionStorageError as exc:
        assert str(exc) == "HITL session file is invalid JSON."


def test_load_invalid_structure_raises_storage_error(tmp_path) -> None:
    storage = HITLSessionStorage(root=tmp_path / "hitl")
    path = tmp_path / "invalid-structure.json"
    path.write_text(json.dumps({"workflow_name": "review", "item_slug": "book"}), encoding="utf-8")

    try:
        storage.load(path)
        assert False, "HITLSessionStorageError expected"
    except HITLSessionStorageError as exc:
        assert str(exc) == "HITL session data is invalid."


def test_load_unknown_status_raises_storage_error(tmp_path) -> None:
    storage = HITLSessionStorage(root=tmp_path / "hitl")
    path = tmp_path / "unknown-status.json"
    path.write_text(
        json.dumps(
            {
                "workflow_name": "review",
                "item_slug": "book",
                "steps": [
                    {"name": "comedy", "status": "unknown", "content": {"response": "..." }},
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        storage.load(path)
        assert False, "HITLSessionStorageError expected"
    except HITLSessionStorageError as exc:
        assert str(exc) == "HITL session data is invalid."
