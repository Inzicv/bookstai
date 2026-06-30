"""Langflow-ready adapter for the Review workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.mock import MockLLMClient
from ..workflows.review import ReviewWorkflow


def run_review_workflow(
    book_slug: str,
    user_opinion: str,
    platform: str,
    memory_root: str | Path = "memory",
    prompt_root: str | Path = "prompts",
) -> dict[str, Any]:
    """Run the existing Review workflow with local mocks only."""

    memory_root_path = Path(memory_root)
    prompt_root_path = Path(prompt_root)

    workflow = ReviewWorkflow(
        memory_root=memory_root_path,
        prompt_root=prompt_root_path,
        llm_client=MockLLMClient(),
    )
    return workflow.run(
        book_slug=book_slug,
        user_opinion=user_opinion,
        platform=platform,
    )
