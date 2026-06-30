"""Learning Loop models for BookstAI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LearningCandidate:
    step_name: str
    status: str
    original_content: Any
    validated_content: Any
    edited_content: Any | None = None
    comment: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_name": self.step_name,
            "status": self.status,
            "original_content": self.original_content,
            "validated_content": self.validated_content,
            "edited_content": self.edited_content,
            "comment": self.comment,
            "metadata": self.metadata,
        }


@dataclass
class LearningExtraction:
    workflow_name: str
    item_slug: str
    candidates: list[LearningCandidate]
    rejected_steps: list[str]
    pending_steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "item_slug": self.item_slug,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "rejected_steps": self.rejected_steps,
            "pending_steps": self.pending_steps,
        }
