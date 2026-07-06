"""Review workflow orchestrator for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from .pitch import PitchWorkflow


class ReviewWorkflow:
    """Compatibility wrapper around the pitch workflow."""

    def __init__(
        self,
        memory_root: Path,
        prompt_root: Path,
        llm_client: LLMClient,
    ) -> None:
        self.pitch_workflow = PitchWorkflow(
            memory_root=memory_root,
            prompt_root=prompt_root,
            llm_client=llm_client,
        )

    def run(
        self,
        book_slug: str | None = None,
        user_opinion: str | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        item_slug = legacy_kwargs.pop("item_slug", None) or book_slug
        summary = legacy_kwargs.pop("summary", None) or user_opinion or ""
        return self.pitch_workflow.run(item_slug=item_slug or "", summary=summary, **legacy_kwargs)

    def run_with_hitl(
        self,
        book_slug: str | None = None,
        user_opinion: str | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        item_slug = legacy_kwargs.pop("item_slug", None) or book_slug
        summary = legacy_kwargs.pop("summary", None) or user_opinion or ""
        return self.pitch_workflow.run_with_hitl(
            item_slug=item_slug or "",
            summary=summary,
            **legacy_kwargs,
        )
