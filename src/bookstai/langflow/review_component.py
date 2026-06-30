"""Langflow-ready adapter for the Review workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.types import ProviderType
from ..llm import create_llm_client
from ..workflows.review import ReviewWorkflow


def run_review_workflow(
    book_slug: str,
    user_opinion: str,
    platform: str,
    memory_root: str | Path = "memory",
    prompt_root: str | Path = "prompts",
    provider: ProviderType = "mock",
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> dict[str, Any]:
    """Run the existing Review workflow with a configurable LLM client."""

    memory_root_path = Path(memory_root)
    prompt_root_path = Path(prompt_root)
    llm_client = create_llm_client(
        provider=provider,
        model=model,
        temperature=temperature,
    )

    workflow = ReviewWorkflow(
        memory_root=memory_root_path,
        prompt_root=prompt_root_path,
        llm_client=llm_client,
    )
    return workflow.run(
        book_slug=book_slug,
        user_opinion=user_opinion,
        platform=platform,
    )
