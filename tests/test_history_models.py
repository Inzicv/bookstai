"""Tests for execution history models."""

from bookstai.history import HistoryEntry


def test_history_entry_conserves_fields() -> None:
    entry = HistoryEntry(command="review", status="success")

    assert entry.command == "review"
    assert entry.status == "success"
    assert entry.created_at


def test_history_entry_to_dict_is_json_compatible() -> None:
    entry = HistoryEntry(command="song", status="failed", error="boom")

    data = entry.to_dict()

    assert data["command"] == "song"
    assert data["status"] == "failed"
    assert data["error"] == "boom"
