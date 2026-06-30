"""JSON exporter for BookstAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JSONExporter:
    """Export workflow data to a JSON file."""

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

        output_path = workflow_dir / f"{item_slug}.json"
        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output_path
