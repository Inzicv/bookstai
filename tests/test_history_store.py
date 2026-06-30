"""Tests for execution history store."""

from __future__ import annotations

import json

from bookstai.history import HistoryEntry, HistoryStore, HistoryStoreError


def test_append_creates_file_and_adds_line(tmp_path) -> None:
    store = HistoryStore(path=tmp_path / "history.jsonl")

    path = store.append(HistoryEntry(command="review", status="success"))

    assert path.exists()
    assert path.read_text(encoding="utf-8").count("\n") == 1


def test_append_twice_adds_two_lines(tmp_path) -> None:
    store = HistoryStore(path=tmp_path / "history.jsonl")
    store.append(HistoryEntry(command="review", status="success"))
    store.append(HistoryEntry(command="song", status="success"))

    assert len(store.read_all()) == 2


def test_read_all_returns_empty_list_when_missing(tmp_path) -> None:
    store = HistoryStore(path=tmp_path / "history.jsonl")

    assert store.read_all() == []


def test_tail_returns_last_entry(tmp_path) -> None:
    store = HistoryStore(path=tmp_path / "history.jsonl")
    store.append(HistoryEntry(command="review", status="success"))
    store.append(HistoryEntry(command="song", status="success"))

    tail = store.tail(limit=1)

    assert len(tail) == 1
    assert tail[0]["command"] == "song"


def test_invalid_json_line_raises_error(tmp_path) -> None:
    path = tmp_path / "history.jsonl"
    path.write_text("{invalid}\n", encoding="utf-8")
    store = HistoryStore(path=path)

    try:
        store.read_all()
        assert False, "HistoryStoreError expected"
    except HistoryStoreError:
        assert True
