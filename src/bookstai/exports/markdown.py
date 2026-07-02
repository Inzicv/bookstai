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
        if workflow_name == "visual":
            return self._build_visual_content(workflow_name, item_slug, data)
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
        song_options_response = self._get_response(data, "song_options")
        technical_data = self._technical_data(data, ["workflow", "book_slug", "song", "song_options"])

        return (
            "# BookstAI — Song Export\n\n"
            "## Métadonnées\n\n"
            f"- Workflow : {workflow_name}\n"
            f"- Livre : {item_slug}\n"
            "- Statut : draft_needs_human_review\n\n"
            "## Song draft\n\n"
            f"{song_response}\n\n"
            "## Song options\n\n"
            f"{song_options_response}\n\n"
            "## Validation humaine\n\n"
            "Ce contenu est un brouillon généré par BookstAI.\n"
            "La créatrice doit le relire, corriger et valider avant publication.\n\n"
            "## Données techniques\n\n"
            "```text\n"
            f"{technical_data}\n"
            "```\n"
        )

    def _build_visual_content(self, workflow_name: str, item_slug: str, data: dict[str, Any]) -> str:
        style_selection = self._get_response(data, "style_selection")
        storyboard = self._get_response(data, "storyboard")
        prompts = self._get_response(data, "prompts")
        technical_data = self._technical_data(
            data,
            ["workflow", "lyrics", "visual_style", "style_selection", "storyboard", "prompts"],
        )

        return (
            "# BookstAI — Visual Export\n\n"
            "## Métadonnées\n\n"
            f"- Workflow : {workflow_name}\n"
            f"- Style : {item_slug}\n"
            "- Statut : draft_needs_human_review\n\n"
            "## Paroles source\n\n"
            f"{data.get('lyrics', '_Non généré_')}\n\n"
            "## Style sélectionné\n\n"
            f"{style_selection}\n\n"
            "## Storyboard\n\n"
            f"{storyboard}\n\n"
            "## Prompts\n\n"
            f"{prompts}\n\n"
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
        section_data = data.get(section)
        if isinstance(section_data, dict):
            response = section_data.get("response")
            if response not in (None, ""):
                return str(response)
            if section_data:
                return pformat(section_data)
        if section_data in (None, ""):
            return "_Non généré_"
        return str(section_data)

    def _nested_value(self, data: dict[str, Any], section: str, key: str) -> Any:
        section_data = data.get(section)
        if isinstance(section_data, dict):
            return section_data.get(key)
        return None

    def _technical_data(self, data: dict[str, Any], excluded_keys: list[str]) -> str:
        technical_data = {key: value for key, value in data.items() if key not in excluded_keys}
        if not technical_data:
            return "{}"
        return pformat(technical_data)
