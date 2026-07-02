"""Markdown exporter for BookstAI."""

from __future__ import annotations

from pathlib import Path
from pprint import pformat
from typing import Any


class MarkdownExporter:
    def __init__(self, output_root: Path) -> None:
        self.output_root = Path(output_root)

    def export(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> Path:
        workflow_dir = self.output_root / workflow_name
        workflow_dir.mkdir(parents=True, exist_ok=True)
        output_path = workflow_dir / f"{item_slug}.md"
        output_path.write_text(self._build_content(workflow_name, item_slug, data), encoding="utf-8")
        return output_path

    def _build_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        if workflow_name == "visual":
            return self._build_visual_content(workflow_name, item_slug, data)
        return f"# BookstAI Export\n\n```text\n{pformat(data)}\n```\n"

    def _build_visual_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        return (
            "# BookstAI - Visual Export\n\n"
            f"- Workflow: {workflow_name}\n"
            f"- Item: {item_slug}\n\n"
            "## Lyrics\n\n"
            f"{data.get('lyrics', '_Not generated_')}\n\n"
            "## Visual Style\n\n"
            f"{pformat(data.get('visual_style', {}))}\n\n"
            "## Storyboard\n\n"
            f"{pformat(data.get('storyboard', {}))}\n\n"
            "## Character Prompts\n\n"
            f"{pformat(data.get('character_prompts', []))}\n\n"
            "## Background Prompts\n\n"
            f"{pformat(data.get('background_prompts', []))}\n\n"
            "## Technical Data\n\n"
            f"```text\n{pformat(data)}\n```\n"
        )
