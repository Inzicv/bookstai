"""Extraction helpers for the Learning Loop."""

from __future__ import annotations

from .models import LearningCandidate, LearningExtraction
from ..hitl import HITLSession, HITLStatus


class LearningExtractor:
    def extract(self, session: HITLSession) -> LearningExtraction:
        candidates: list[LearningCandidate] = []
        rejected_steps: list[str] = []
        pending_steps: list[str] = []

        for step in session._steps.values():
            if step.status == HITLStatus.APPROVED:
                candidates.append(
                    LearningCandidate(
                        step_name=step.name,
                        status=step.status.value,
                        original_content=step.content,
                        validated_content=step.content,
                        edited_content=None,
                        comment=step.comment,
                        metadata=step.metadata,
                    )
                )
            elif step.status == HITLStatus.EDITED:
                if step.edited_content is None:
                    pending_steps.append(step.name)
                    continue
                candidates.append(
                    LearningCandidate(
                        step_name=step.name,
                        status=step.status.value,
                        original_content=step.content,
                        validated_content=step.edited_content,
                        edited_content=step.edited_content,
                        comment=step.comment,
                        metadata=step.metadata,
                    )
                )
            elif step.status == HITLStatus.REJECTED:
                rejected_steps.append(step.name)
            else:
                pending_steps.append(step.name)

        return LearningExtraction(
            workflow_name=session.workflow_name,
            item_slug=session.item_slug,
            candidates=candidates,
            rejected_steps=rejected_steps,
            pending_steps=pending_steps,
        )
