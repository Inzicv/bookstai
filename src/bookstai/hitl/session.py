"""Human In The Loop session management for BookstAI."""

from __future__ import annotations

from typing import Any

from ..core.errors import HITLStepNotFoundError
from .models import HITLStep, HITLStatus


class HITLSession:
    def __init__(self, workflow_name: str, item_slug: str) -> None:
        self.workflow_name = workflow_name
        self.item_slug = item_slug
        self._steps: dict[str, HITLStep] = {}

    def add_step(
        self,
        name: str,
        content: Any,
        metadata: dict[str, Any] | None = None,
    ) -> HITLStep:
        step = HITLStep(
            name=name,
            content=content,
            metadata=metadata or {},
        )
        self._steps[name] = step
        return step

    def get_step(self, name: str) -> HITLStep:
        try:
            return self._steps[name]
        except KeyError as exc:
            raise HITLStepNotFoundError(f"HITL step '{name}' was not found.") from exc

    def approve_step(self, name: str, comment: str | None = None) -> HITLStep:
        step = self.get_step(name)
        step.status = HITLStatus.APPROVED
        step.comment = comment
        return step

    def reject_step(self, name: str, comment: str | None = None) -> HITLStep:
        step = self.get_step(name)
        step.status = HITLStatus.REJECTED
        step.comment = comment
        return step

    def edit_step(
        self,
        name: str,
        edited_content: Any,
        comment: str | None = None,
    ) -> HITLStep:
        step = self.get_step(name)
        step.status = HITLStatus.EDITED
        step.edited_content = edited_content
        step.comment = comment
        return step

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "item_slug": self.item_slug,
            "steps": [
                {
                    "name": step.name,
                    "status": step.status.value,
                    "content": step.content,
                    "edited_content": step.edited_content,
                    "comment": step.comment,
                    "metadata": step.metadata,
                }
                for step in self._steps.values()
            ],
        }
