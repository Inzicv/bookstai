"""Tests for JSONExporter."""

import json
from pathlib import Path

from bookstai.exports.json import JSONExporter


def test_exports_json_file(tmp_path: Path) -> None:
    exporter = JSONExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="alchemised",
        data={
            "workflow": "review",
            "book_slug": "alchemised",
            "review": {"response": "Review générée"},
            "social": {"response": "Caption générée"},
        },
    )

    assert path == tmp_path / "outputs" / "review" / "alchemised.json"
    assert path.exists()
    assert path.is_file()


def test_creates_workflow_directory_automatically(tmp_path: Path) -> None:
    exporter = JSONExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="song",
        item_slug="alchemised",
        data={"workflow": "song"},
    )

    assert (tmp_path / "outputs" / "song").exists()
    assert path.parent == tmp_path / "outputs" / "song"


def test_returns_path_object(tmp_path: Path) -> None:
    exporter = JSONExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review"},
    )

    assert isinstance(path, Path)


def test_exported_json_is_readable(tmp_path: Path) -> None:
    exporter = JSONExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="alchemised",
        data={
            "workflow": "review",
            "book_slug": "alchemised",
            "social": {"response": "Caption générée"},
        },
    )

    content = path.read_text(encoding="utf-8")
    parsed = json.loads(content)

    assert parsed["workflow"] == "review"
    assert parsed["book_slug"] == "alchemised"
    assert parsed["social"]["response"] == "Caption générée"


def test_supports_nested_dictionary_data(tmp_path: Path) -> None:
    exporter = JSONExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="nested",
        data={
            "level1": {
                "level2": {
                    "value": 42,
                }
            }
        },
    )

    parsed = json.loads(path.read_text(encoding="utf-8"))

    assert parsed["level1"]["level2"]["value"] == 42


def test_preserves_accents_with_ensure_ascii_false(tmp_path: Path) -> None:
    exporter = JSONExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="accents",
        data={
            "workflow": "review",
            "title": "Céline et l’été",
        },
    )

    content = path.read_text(encoding="utf-8")

    assert "Céline" in content
    assert "\\u00e9" not in content
