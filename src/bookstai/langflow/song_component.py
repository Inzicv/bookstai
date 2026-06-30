"""Langflow-ready adapter for the Song workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..image.mock_backend import MockImageBackend
from ..llm.mock import MockLLMClient
from ..workflows.song import SongWorkflow


def run_song_workflow(
    book_slug: str,
    spoiler_mode: str,
    prompt_type: str,
    platform: str,
    memory_root: str | Path = "memory",
    prompt_root: str | Path = "prompts",
    image_path: str | Path = "outputs/mock/image.png",
) -> dict[str, Any]:
    """Run the existing Song workflow with local mocks only."""

    memory_root_path = Path(memory_root)
    prompt_root_path = Path(prompt_root)

    workflow = SongWorkflow(
        memory_root=memory_root_path,
        prompt_root=prompt_root_path,
        llm_client=MockLLMClient(),
        image_backend=MockImageBackend(image_path=str(Path(image_path))),
    )
    return workflow.run(
        book_slug=book_slug,
        spoiler_mode=spoiler_mode,
        prompt_type=prompt_type,
        platform=platform,
    )
