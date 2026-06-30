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
        content = self._build_content(workflow_name=workflow_name, item_slug=item_slug, data=data)
        output_path.write_text(content, encoding="utf-8")
        return output_path

    def _build_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        if workflow_name == "review":
            return self._build_review_content(workflow_name, item_slug, data)
        if workflow_name == "song":
            return self._build_song_content(workflow_name, item_slug, data)
        return self._build_generic_content(workflow_name, item_slug, data)

    def _build_review_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        review_response = self._get_response(data, "review")
        social_response = self._get_response(data, "social")
        comedy_response = self._get_response(data, "comedy")
        technical_data = self._technical_data(data, ["workflow", "book_slug", "review", "social", "comedy"])

        return (
            "# BookstAI — Review Export\n\n"
            "## Métadonnées\n\n"
            f"- Workflow : {workflow_name}\n"
            f"- Livre : {item_slug}\n"
            "- Statut : draft_needs_human_review\n\n"
            "## Review draft\n\n"
            f"{review_response}\n\n"
            "## Social media draft\n\n"
            f"{social_response}\n\n"
            "## Comedy room\n\n"
            f"{comedy_response}\n\n"
            "## Validation humaine\n\n"
            "Ce contenu est un brouillon généré par BookstAI.\n"
            "La créatrice doit le relire, corriger et valider avant publication.\n\n"
            "## Données techniques\n\n"
            "```text\n"
            f"{technical_data}\n"
            "```\n"
        )

    def _build_song_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        song_response = self._get_response(data, "song")
        art_direction_response = self._get_response(data, "art_direction")
        image_prompt_response = self._get_response(data, "image_prompt")
        social_response = self._get_response(data, "social")
        comedy_response = self._get_response(data, "comedy")
        image_backend = self._display_value(self._nested_value(data, "image", "backend"))
        image_path = self._display_value(self._nested_value(data, "image", "image_path"))
        technical_data = self._technical_data(
            data,
            ["workflow", "book_slug", "song", "art_direction", "image_prompt", "image", "social", "comedy"],
        )

        return (
            "# BookstAI — Song Export\n\n"
            "## Métadonnées\n\n"
            f"- Workflow : {workflow_name}\n"
            f"- Livre : {item_slug}\n"
            "- Statut : draft_needs_human_review\n\n"
            "## Song draft\n\n"
            f"{song_response}\n\n"
            "## Art direction\n\n"
            f"{art_direction_response}\n\n"
            "## Image prompt\n\n"
            f"{image_prompt_response}\n\n"
            "## Image result\n\n"
            f"- Backend : {image_backend}\n"
            f"- Image path : {image_path}\n\n"
            "## Social media draft\n\n"
            f"{social_response}\n\n"
            "## Comedy room\n\n"
            f"{comedy_response}\n\n"
            "## Validation humaine\n\n"
            "Ce contenu est un brouillon généré par BookstAI.\n"
            "La créatrice doit le relire, corriger et valider avant publication.\n\n"
            "## Données techniques\n\n"
            "```text\n"
            f"{technical_data}\n"
            "```\n"
        )

    def _build_generic_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        return (
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

    def _get_response(self, data: dict[str, Any], section: str) -> str:
        response = self._nested_value(data, section, "response")
        if response in (None, ""):
            return "_Non généré_"
        return str(response)

    def _nested_value(self, data: dict[str, Any], section: str, key: str) -> Any:
        section_data = data.get(section)
        if isinstance(section_data, dict):
            return section_data.get(key)
        return None

    def _display_value(self, value: Any) -> str:
        if value in (None, ""):
            return "_Non généré_"
        return str(value)

    def _technical_data(self, data: dict[str, Any], excluded_keys: list[str]) -> str:
        technical_data = {key: value for key, value in data.items() if key not in excluded_keys}
        if not technical_data:
            return "{}"
        return pformat(technical_data)
