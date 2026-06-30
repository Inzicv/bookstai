"""Langflow-ready adapter for the Song workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.types import ProviderType
from ..image.mock_backend import MockImageBackend
from ..llm import create_llm_client
from ..workflows.song import SongWorkflow
from .paths import resolve_bookstai_path


def run_song_workflow(
    book_slug: str,
    spoiler_mode: str,
    prompt_type: str,
    platform: str,
    memory_root: str | Path = "memory",
    prompt_root: str | Path = "prompts",
    image_path: str | Path = "outputs/mock/image.png",
    provider: ProviderType = "mock",
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> dict[str, Any]:
    """Run the existing Song workflow with a configurable LLM client."""

    memory_root_path = resolve_bookstai_path(memory_root, "memory")
    prompt_root_path = resolve_bookstai_path(prompt_root, "prompts")
    llm_client = create_llm_client(
        provider=provider,
        model=model,
        temperature=temperature,
    )

    workflow = SongWorkflow(
        memory_root=memory_root_path,
        prompt_root=prompt_root_path,
        llm_client=llm_client,
        image_backend=MockImageBackend(image_path=str(Path(image_path))),
    )
    return workflow.run(
        book_slug=book_slug,
        spoiler_mode=spoiler_mode,
        prompt_type=prompt_type,
        platform=platform,
    )
