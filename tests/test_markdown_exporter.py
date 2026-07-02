"""Tests for MarkdownExporter."""

from pathlib import Path

from bookstai.exports.markdown import MarkdownExporter


def test_markdown_exporter_writes_readable_review_export(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")
    data = {
        "workflow": "review",
        "book_slug": "alchemised",
        "comedy": {"response": "Idées drôles"},
        "review": {"response": "Review générée"},
        "social": {"response": "Caption générée"},
    }

    path = exporter.export(workflow_name="review", item_slug="alchemised", data=data)

    content = path.read_text(encoding="utf-8")

    assert path.exists()
    assert "# BookstAI — Review Export" in content
    assert "## Métadonnées" in content
    assert "Workflow : review" in content
    assert "Livre : alchemised" in content
    assert "draft_needs_human_review" in content
    assert "## Review draft" in content
    assert "Review générée" in content
    assert "## Comedy room" in content
    assert "## Validation humaine" in content


def test_markdown_exporter_writes_readable_song_export(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")
    data = {
        "workflow": "song",
        "book_slug": "alchemised",
        "comedy": {"response": "Idées drôles"},
        "song": {"response": "Chanson générée"},
        "social": {"response": "Caption générée"},
    }

    path = exporter.export(workflow_name="song", item_slug="alchemised", data=data)

    content = path.read_text(encoding="utf-8")

    assert path.exists()
    assert "# BookstAI — Song Export" in content
    assert "## Métadonnées" in content
    assert "Workflow : song" in content
    assert "Livre : alchemised" in content
    assert "draft_needs_human_review" in content
    assert "## Song draft" in content
    assert "Chanson générée" in content
    assert "## Storyboard" not in content
    assert "## Prompts" not in content
    assert "## Validation humaine" in content
    assert "## Données techniques" in content


def test_markdown_exporter_handles_missing_sections_gracefully(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="review",
        item_slug="minimal",
        data={
            "workflow": "review",
            "book_slug": "minimal",
        },
    )

    content = path.read_text(encoding="utf-8")

    assert "_Non généré_" in content
    assert "Review draft" in content
    assert "Social media draft" in content
    assert "Comedy room" in content


def test_markdown_exporter_keeps_generic_fallback_for_unknown_workflow(tmp_path: Path) -> None:
    exporter = MarkdownExporter(output_root=tmp_path / "outputs")

    path = exporter.export(
        workflow_name="unknown",
        item_slug="example",
        data={"hello": "world"},
    )

    content = path.read_text(encoding="utf-8")

    assert "# BookstAI Export" in content
    assert "## Workflow" in content
    assert "unknown" in content
    assert "## Item" in content
    assert "example" in content
    assert "## Data" in content
    assert "hello" in content
    assert "world" in content
