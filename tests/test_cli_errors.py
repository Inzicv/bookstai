"""Tests for CLI error handling."""

from __future__ import annotations

from bookstai import cli
from bookstai.core.errors import BookstAIError


def test_cli_bookstai_error_returns_one_and_prints_message(monkeypatch, capsys, tmp_path) -> None:
    class DummyWorkflow:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def run(self, **kwargs):
            raise BookstAIError("boom")

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: type("S", (), {"memory_root": tmp_path / "memory"})())
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "client")

    exit_code = cli.main(["review", "--book", "book", "--opinion", "ok", "--platform", "tiktok", "--no-history"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "BookstAI error: boom" in captured.out
    assert "Traceback" not in captured.out
