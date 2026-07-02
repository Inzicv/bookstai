"""Tests for Learning CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from bookstai import cli
from bookstai.hitl import HITLSession
from bookstai.learning import LearningCandidate, LearningExtraction


class DummyStorage:
    def __init__(self, session: HITLSession) -> None:
        self.session = session
        self.loaded_paths: list[Path] = []

    def load(self, path):
        self.loaded_paths.append(Path(path))
        return self.session


class DummyExtractor:
    def __init__(self) -> None:
        self.loaded_sessions = []

    def extract(self, session):
        self.loaded_sessions.append(session)
        return LearningExtraction(
            workflow_name=session.workflow_name,
            item_slug=session.item_slug,
            candidates=[
                LearningCandidate(
                    step_name="review",
                    status="edited",
                    original_content="original",
                    validated_content="valid",
                    edited_content="valid",
                    comment="ok",
                )
            ],
            rejected_steps=["social"],
            pending_steps=["comedy"],
        )


def _hitl_session(tmp_path: Path) -> Path:
    path = tmp_path / "hitl.json"
    path.write_text(
        json.dumps(
            {
                "workflow_name": "review",
                "item_slug": "book",
                "steps": [
                    {
                        "name": "review",
                        "status": "edited",
                        "content": "original",
                        "edited_content": "valid",
                        "comment": "ok",
                        "metadata": {},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_parser_accepts_learning_subcommands() -> None:
    parser = cli.build_parser()

    assert parser.parse_args(["learning", "extract", "--hitl-file", "x.json"]).learning_command == "extract"
    assert parser.parse_args(["learning", "draft", "--hitl-file", "x.json"]).learning_command == "draft"
    assert parser.parse_args([
        "learning",
        "apply",
        "--draft-file",
        "draft.md",
        "--memory-file",
        "books/book.md",
    ]).learning_command == "apply"


def test_parser_requires_learning_arguments() -> None:
    parser = cli.build_parser()

    for argv in (
        ["learning", "extract"],
        ["learning", "draft"],
        ["learning", "apply", "--draft-file", "draft.md"],
    ):
        try:
            parser.parse_args(argv)
            assert False, "SystemExit expected"
        except SystemExit as exc:
            assert exc.code != 0


def test_parser_accepts_learning_apply_memory_root() -> None:
    parser = cli.build_parser()
    args = parser.parse_args([
        "learning",
        "apply",
        "--draft-file",
        "draft.md",
        "--memory-file",
        "books/book.md",
        "--memory-root",
        "custom-memory",
    ])

    assert args.memory_root == "custom-memory"


def test_learning_extract_outputs_json_compatible_structure(monkeypatch, tmp_path) -> None:
    session_path = _hitl_session(tmp_path)
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="review", content="original")
    session.edit_step("review", edited_content="valid", comment="ok")
    storage = DummyStorage(session)
    extractor = DummyExtractor()
    captured = {}

    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "LearningExtractor", lambda: extractor)
    monkeypatch.setattr(cli, "pprint", lambda value: captured.setdefault("value", value))

    assert cli.main(["learning", "extract", "--hitl-file", str(session_path)]) == 0
    assert storage.loaded_paths == [session_path]
    assert extractor.loaded_sessions == [session]
    assert captured["value"]["candidates"][0]["step_name"] == "review"


def test_learning_draft_writes_markdown(monkeypatch, tmp_path) -> None:
    session_path = _hitl_session(tmp_path)
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="review", content="original")
    session.edit_step("review", edited_content="valid", comment="ok")
    storage = DummyStorage(session)
    extractor = DummyExtractor()
    output_root = tmp_path / "learning-output"
    captured = {}

    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "LearningExtractor", lambda: extractor)
    monkeypatch.setattr(cli, "pprint", lambda value: captured.setdefault("value", value))

    assert cli.main([
        "learning",
        "draft",
        "--hitl-file",
        str(session_path),
        "--output-root",
        str(output_root),
    ]) == 0

    draft_path = output_root / "review" / "book-learning-draft.md"
    assert draft_path.exists()
    assert "Learning Draft" in draft_path.read_text(encoding="utf-8")
    assert captured["value"]["learning_draft"] == str(draft_path)


def test_learning_apply_writes_memory_with_backup(monkeypatch, tmp_path) -> None:
    draft_path = tmp_path / "draft.md"
    draft_path.write_text("# draft", encoding="utf-8")
    memory_root = tmp_path / "memory"
    memory_file = memory_root / "books" / "book.md"
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    memory_file.write_text("old content", encoding="utf-8")
    captured = {}

    monkeypatch.setattr(cli, "pprint", lambda value: captured.setdefault("value", value))

    assert cli.main([
        "learning",
        "apply",
        "--draft-file",
        str(draft_path),
        "--memory-file",
        "books/book.md",
        "--memory-root",
        str(memory_root),
    ]) == 0

    result = captured["value"]
    assert result["draft_path"] == str(draft_path)
    assert result["memory_path"] == str(memory_file.resolve())
    assert result["backup_path"] is not None
    assert result["applied"] is True
    assert "Learning Update" in memory_file.read_text(encoding="utf-8")


def test_learning_commands_do_not_use_workflows(monkeypatch, tmp_path) -> None:
    session_path = _hitl_session(tmp_path)
    session = HITLSession(workflow_name="review", item_slug="book")
    storage = DummyStorage(session)
    extractor = DummyExtractor()

    monkeypatch.setattr(cli, "HITLSessionStorage", lambda: storage)
    monkeypatch.setattr(cli, "LearningExtractor", lambda: extractor)
    monkeypatch.setattr(cli, "ReviewWorkflow", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("ReviewWorkflow should not be used")))
    monkeypatch.setattr(cli, "SongWorkflow", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("SongWorkflow should not be used")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: (_ for _ in ()).throw(AssertionError("OpenAI should not be used")))
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    assert cli.main(["learning", "extract", "--hitl-file", str(session_path)]) == 0
