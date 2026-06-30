"""Tests for HITL CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from bookstai import cli
from bookstai.hitl import HITLSession


class DummyStorage:
    def __init__(self) -> None:
        self.loaded_paths: list[Path] = []
        self.saved: list[tuple[str, Path]] = []

    def load(self, path):
        self.loaded_paths.append(Path(path))
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return HITLSession.from_dict(data)

    def save_to_path(self, session, path):
        path = Path(path)
        self.saved.append((session.to_dict()["steps"][0]["status"], path))
        path.write_text(json.dumps(session.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return path


def test_parser_accepts_hitl_subcommands() -> None:
    parser = cli.build_parser()

    assert parser.parse_args(["hitl", "show", "--file", "x.json"]).hitl_command == "show"
    assert parser.parse_args(["hitl", "approve", "--file", "x.json", "--step", "s"]).hitl_command == "approve"
    assert parser.parse_args(["hitl", "reject", "--file", "x.json", "--step", "s"]).hitl_command == "reject"
    assert parser.parse_args(["hitl", "edit", "--file", "x.json", "--step", "s", "--content", "c"]).hitl_command == "edit"


def test_parser_requires_hitl_arguments() -> None:
    parser = cli.build_parser()

    for argv in (
        ["hitl", "show"],
        ["hitl", "approve", "--file", "x.json"],
        ["hitl", "reject", "--file", "x.json"],
        ["hitl", "edit", "--file", "x.json", "--step", "s"],
    ):
        try:
            parser.parse_args(argv)
            assert False, "SystemExit expected"
        except SystemExit as exc:
            assert exc.code != 0


def test_hitl_show_returns_zero(monkeypatch, tmp_path) -> None:
    session_path = tmp_path / "session.json"
    session_path.write_text(
        json.dumps(
            {
                "workflow_name": "review",
                "item_slug": "book",
                "steps": [{"name": "review", "status": "pending", "content": {"text": "ok"}}],
            }
        ),
        encoding="utf-8",
    )

    storage = DummyStorage()
    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    assert cli.main(["hitl", "show", "--file", str(session_path)]) == 0
    assert storage.loaded_paths == [session_path]
    assert storage.saved == []


def test_hitl_approve_updates_and_saves(monkeypatch, tmp_path) -> None:
    session_path = tmp_path / "session.json"
    session_path.write_text(
        json.dumps(
            {
                "workflow_name": "review",
                "item_slug": "book",
                "steps": [{"name": "review", "status": "pending", "content": {"text": "ok"}}],
            }
        ),
        encoding="utf-8",
    )

    storage = DummyStorage()
    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    assert cli.main(["hitl", "approve", "--file", str(session_path), "--step", "review"]) == 0
    updated = json.loads(session_path.read_text(encoding="utf-8"))
    assert updated["steps"][0]["status"] == "approved"
    assert storage.saved[0][0] == "approved"


def test_hitl_reject_keeps_comment_and_saves(monkeypatch, tmp_path) -> None:
    session_path = tmp_path / "session.json"
    session_path.write_text(
        json.dumps(
            {
                "workflow_name": "review",
                "item_slug": "book",
                "steps": [{"name": "social", "status": "pending", "content": {"text": "ok"}}],
            }
        ),
        encoding="utf-8",
    )

    storage = DummyStorage()
    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    assert cli.main(["hitl", "reject", "--file", str(session_path), "--step", "social", "--comment", "Pas assez fort"]) == 0
    updated = json.loads(session_path.read_text(encoding="utf-8"))
    assert updated["steps"][0]["status"] == "rejected"
    assert updated["steps"][0]["comment"] == "Pas assez fort"


def test_hitl_edit_keeps_original_content_and_saves(monkeypatch, tmp_path) -> None:
    session_path = tmp_path / "session.json"
    session_path.write_text(
        json.dumps(
            {
                "workflow_name": "song",
                "item_slug": "book",
                "steps": [{"name": "song", "status": "pending", "content": {"text": "original"}}],
            }
        ),
        encoding="utf-8",
    )

    storage = DummyStorage()
    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    assert cli.main(["hitl", "edit", "--file", str(session_path), "--step", "song", "--content", "new text"]) == 0
    updated = json.loads(session_path.read_text(encoding="utf-8"))
    assert updated["steps"][0]["status"] == "edited"
    assert updated["steps"][0]["content"] == {"text": "original"}
    assert updated["steps"][0]["edited_content"] == "new text"


def test_hitl_unknown_step_raises(monkeypatch, tmp_path) -> None:
    session_path = tmp_path / "session.json"
    session_path.write_text(
        json.dumps(
            {
                "workflow_name": "review",
                "item_slug": "book",
                "steps": [{"name": "review", "status": "pending", "content": {"text": "ok"}}],
            }
        ),
        encoding="utf-8",
    )

    storage = DummyStorage()
    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    assert cli.main(["hitl", "approve", "--file", str(session_path), "--step", "missing"]) == 1
