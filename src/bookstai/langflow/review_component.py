"""Compatibility Langflow review component for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.mock import MockLLMClient
from ..workflows.pitch import PitchWorkflow


class BookstAIReviewComponent:
    display_name = "BookstAI Pitch"

    def run_review_workflow(
        self,
        item_slug: str,
        summary: str,
        provider: str = "mock",
        model: str | None = None,
        temperature: float = 0.7,
        memory_root: str | Path = "memory",
        prompt_root: str | Path = "prompts",
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        workflow = PitchWorkflow(
            memory_root=Path(memory_root),
            prompt_root=Path(prompt_root),
            llm_client=MockLLMClient(),
        )
        return workflow.run(item_slug=item_slug, summary=summary, **legacy_kwargs)
