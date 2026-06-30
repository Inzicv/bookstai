"""Tests for ExportService."""

import json
from pathlib import Path

import pytest

from bookstai.core.errors import InvalidExportFormatError
from bookstai.exports.service import ExportService


def test_export_markdown_only(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")

    paths = service.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review", "book_slug": "alchemised"},
        formats=["markdown"],
    )

    assert list(paths.keys()) == ["markdown"]
    assert paths["markdown"].suffix == ".md"
    assert paths["markdown"].exists()


def test_export_json_only(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")

    paths = service.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review", "book_slug": "alchemised"},
        formats=["json"],
    )

    assert list(paths.keys()) == ["json"]
    assert paths["json"].suffix == ".json"
    assert paths["json"].exists()


def test_export_markdown_and_json(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")

    paths = service.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review", "book_slug": "alchemised"},
        formats=["markdown", "json"],
    )

    assert list(paths.keys()) == ["markdown", "json"]
    assert paths["markdown"].exists()
    assert paths["json"].exists()


def test_export_returns_dictionary(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")

    paths = service.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review", "book_slug": "alchemised"},
        formats=["markdown"],
    )

    assert isinstance(paths, dict)
    assert isinstance(paths["markdown"], Path)


def test_duplicate_formats_are_ignored(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")

    paths = service.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review", "book_slug": "alchemised"},
        formats=["markdown", "markdown", "json", "json"],
    )

    assert list(paths.keys()) == ["markdown", "json"]


def test_invalid_format_raises_error(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")

    with pytest.raises(InvalidExportFormatError):
        service.export(
            workflow_name="review",
            item_slug="alchemised",
            data={"workflow": "review"},
            formats=["xml"],
        )


def test_exported_files_keep_data(tmp_path: Path) -> None:
    service = ExportService(output_root=tmp_path / "outputs")
    data = {
        "workflow": "review",
        "book_slug": "alchemised",
        "nested": {"level2": {"value": 42}},
    }

    paths = service.export(
        workflow_name="review",
        item_slug="alchemised",
        data=data,
        formats=["markdown", "json"],
    )

    markdown_content = paths["markdown"].read_text(encoding="utf-8")
    json_content = json.loads(paths["json"].read_text(encoding="utf-8"))

    assert "review" in markdown_content
    assert "alchemised" in markdown_content
    assert "42" in markdown_content
    assert json_content["nested"]["level2"]["value"] == 42
