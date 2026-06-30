"""Markdown exporter for BookstAI."""

from __future__ import annotations

from pathlib import Path
from pprint import pformat
from typing import Any


class MarkdownExporter:
    """Export workflow data to a Markdown file."""

    def __init__(self, output_root: Path) -> None:
        self.output_root = Path(output_root)

    def export(
        self,
        workflow_name: str,
        item_slug: str,
        data: dict[str, Any],
    ) -> Path:
        workflow_dir = self.output_root / workflow_name
        workflow_dir.mkdir(parents=True, exist_ok=True)

        output_path = workflow_dir / f"{item_slug}.md"
        content = (
            "# BookstAI Export\n\n"
            "## Workflow\n\n"
            f"{workflow_name}\n\n"
            "## Item\n\n"
            f"{item_slug}\n\n"
            "## Data\n\n"
            "```text\n"
            f"{pformat(data)}\n"
            "```\n"
        )
        output_path.write_text(content, encoding="utf-8")
        return output_path
