"""Tests for history CLI commands."""

from __future__ import annotations

import json

from bookstai import cli


def test_parser_accepts_history_commands() -> None:
    parser = cli.build_parser()

    assert parser.parse_args(["history", "show"]).history_command == "show"
    assert parser.parse_args(["history", "tail"]).history_command == "tail"


def test_history_tail_accepts_limit() -> None:
    parser = cli.build_parser()
    args = parser.parse_args(["history", "tail", "--limit", "20"])

    assert args.limit == 20


def test_history_show_returns_zero(monkeypatch, tmp_path) -> None:
    history_file = tmp_path / "history.jsonl"
    history_file.write_text(json.dumps({"command": "review", "status": "success"}) + "\n", encoding="utf-8")
    captured = {}

    monkeypatch.setattr(cli, "pprint", lambda value: captured.setdefault("value", value))

    assert cli.main(["history", "show", "--file", str(history_file)]) == 0
    assert captured["value"][0]["command"] == "review"


def test_history_tail_returns_zero_and_uses_file(monkeypatch, tmp_path) -> None:
    history_file = tmp_path / "history.jsonl"
    history_file.write_text(
        json.dumps({"command": "review", "status": "success"}) + "\n" + json.dumps({"command": "song", "status": "success"}) + "\n",
        encoding="utf-8",
    )
    captured = {}

    monkeypatch.setattr(cli, "pprint", lambda value: captured.setdefault("value", value))

    assert cli.main(["history", "tail", "--file", str(history_file), "--limit", "1"]) == 0
    assert captured["value"][0]["command"] == "song"
