"""Langflow-ready adapter for the Song workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.types import ImageBackendType, ProviderType
from ..image import create_image_backend
from ..llm import create_llm_client
from ..workflows.song import SongWorkflow
from .paths import resolve_bookstai_path


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


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
    image_backend: ImageBackendType = "mock",
    comfyui_url: str = "http://127.0.0.1:8188",
    comfyui_workflow_path: str | Path | None = None,
    image_output_dir: str | Path = "outputs/images",
    image_timeout: float = 60.0,
    image_poll_interval: float = 1.0,
    hitl: bool = False,
) -> dict[str, Any]:
    """Run the existing Song workflow with a configurable LLM client."""

    memory_root_path = resolve_bookstai_path(memory_root, "memory")
    prompt_root_path = resolve_bookstai_path(prompt_root, "prompts")
    llm_client = create_llm_client(
        provider=provider,
        model=model,
        temperature=temperature,
    )
    image_backend_instance = create_image_backend(
        backend=image_backend,
        image_path=image_path,
        comfyui_url=comfyui_url,
        workflow_path=comfyui_workflow_path,
        output_dir=image_output_dir,
        timeout=image_timeout,
        poll_interval=image_poll_interval,
    )

    workflow = SongWorkflow(
        memory_root=memory_root_path,
        prompt_root=prompt_root_path,
        llm_client=llm_client,
        image_backend=image_backend_instance,
    )
    if _to_bool(hitl):
        return workflow.run_with_hitl(
            book_slug=book_slug,
            spoiler_mode=spoiler_mode,
            prompt_type=prompt_type,
            platform=platform,
        )
    return workflow.run(
        book_slug=book_slug,
        spoiler_mode=spoiler_mode,
        prompt_type=prompt_type,
        platform=platform,
    )
