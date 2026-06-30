"""Markdown draft writer for Learning Loop outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import LearningExtraction


def _format_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        return str(value)


class LearningDraftWriter:
    def __init__(self, output_root: str | Path = "outputs/learning") -> None:
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)

    def write(self, extraction: LearningExtraction) -> Path:
        workflow_dir = self.output_root / extraction.workflow_name
        workflow_dir.mkdir(parents=True, exist_ok=True)
        output_path = workflow_dir / f"{extraction.item_slug}-learning-draft.md"
        output_path.write_text(self._build_content(extraction), encoding="utf-8")
        return output_path

    def _build_content(self, extraction: LearningExtraction) -> str:
        lines: list[str] = [
            f"# Learning Draft - {extraction.workflow_name} / {extraction.item_slug}",
            "",
            "## Contexte",
            "",
            f"- **Workflow :** {extraction.workflow_name}",
            f"- **Livre :** {extraction.item_slug}",
            "",
            "## Candidates d'apprentissage",
            "",
        ]

        if extraction.candidates:
            for candidate in extraction.candidates:
                lines.extend(
                    [
                        f"### Étape : {candidate.step_name}",
                        "",
                        f"- **Statut :** {candidate.status}",
                        f"- **Commentaire :** {candidate.comment or ''}",
                        "",
                        "#### Contenu original",
                        "",
                        "```text",
                        _format_content(candidate.original_content),
                        "```",
                        "",
                        "#### Contenu validé",
                        "",
                        "```text",
                        _format_content(candidate.validated_content),
                        "```",
                        "",
                    ]
                )
        else:
            lines.extend(
                [
                    "Aucune candidate d'apprentissage exploitable.",
                    "",
                ]
            )

        lines.extend(
            [
                "## Étapes rejetées",
                "",
            ]
        )
        if extraction.rejected_steps:
            lines.extend([f"- {step}" for step in extraction.rejected_steps])
        else:
            lines.append("- Aucune")

        lines.extend(
            [
                "",
                "## Étapes en attente",
                "",
            ]
        )
        if extraction.pending_steps:
            lines.extend([f"- {step}" for step in extraction.pending_steps])
        else:
            lines.append("- Aucune")

        lines.extend(
            [
                "",
                "## Instruction",
                "",
                "Ce fichier est un brouillon.",
                "",
                "Il ne modifie pas encore la mémoire BookstAI.",
                "",
                "Relire, corriger puis appliquer explicitement si le contenu est pertinent.",
                "",
            ]
        )
        return "\n".join(lines)
