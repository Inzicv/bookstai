"""Export service for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.errors import InvalidExportFormatError
from .json import JSONExporter
from .markdown import MarkdownExporter

SUPPORTED_FORMATS = ("markdown", "json")


class ExportService:
    """Export workflow data in one or more formats."""

    def __init__(self, output_root: Path) -> None:
        self.markdown_exporter = MarkdownExporter(output_root=output_root)
        self.json_exporter = JSONExporter(output_root=output_root)

    def export(
        self,
        workflow_name: str,
        item_slug: str,
        data: dict[str, Any],
        formats: list[str],
    ) -> dict[str, Path]:
        paths: dict[str, Path] = {}
        seen: set[str] = set()

        for format_name in formats:
            if format_name in seen:
                continue
            seen.add(format_name)

            if format_name == "markdown":
                paths["markdown"] = self.markdown_exporter.export(
                    workflow_name=workflow_name,
                    item_slug=item_slug,
                    data=data,
                )
            elif format_name == "json":
                paths["json"] = self.json_exporter.export(
                    workflow_name=workflow_name,
                    item_slug=item_slug,
                    data=data,
                )
            else:
                raise InvalidExportFormatError("Invalid export format.")

        return paths
