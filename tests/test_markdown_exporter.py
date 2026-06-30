"""Tests for MarkdownExporter."""

from pathlib import Path

from bookstai.exports.markdown import MarkdownExporter


def test_exports_markdown_file(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

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

    assert path == tmp_path / "outputs" / "review" / "alchemised.md"
    assert path.exists()
    assert path.is_file()


def test_creates_workflow_directory_automatically(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="song",
        item_slug="alchemised",
        data={"workflow": "song"},
    )

    assert (tmp_path / "outputs" / "song").exists()
    assert path.parent == tmp_path / "outputs" / "song"


def test_returns_path_object(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="alchemised",
        data={"workflow": "review"},
    )

    assert isinstance(path, Path)


def test_exported_content_contains_workflow_item_and_data(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

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

    assert "# BookstAI Export" in content
    assert "review" in content
    assert "alchemised" in content
    assert "Caption générée" in content


def test_supports_nested_dictionary_data(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

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

    content = path.read_text(encoding="utf-8")

    assert "level1" in content
    assert "level2" in content
    assert "42" in content
