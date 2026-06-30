"""Project pre-check helpers for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REQUIRED_AGENT_PROMPTS = [
    "agents/comedy_room.md",
    "agents/review_writer.md",
    "agents/song_writer.md",
    "agents/art_director.md",
    "agents/prompt_maker.md",
    "agents/social_media.md",
    "agents/memory_manager.md",
]


def check_required_agent_prompts(prompt_root: str | Path = "prompts") -> dict[str, Any]:
    root = Path(prompt_root)
    required_prompts = list(REQUIRED_AGENT_PROMPTS)
    existing_prompts: list[str] = []
    missing_prompts: list[str] = []

    for prompt in required_prompts:
        prompt_path = root / Path(prompt)
        if prompt_path.exists():
            existing_prompts.append(prompt)
        else:
            missing_prompts.append(prompt)

    return {
        "ok": not missing_prompts,
        "prompt_root": str(root),
        "required_prompts": required_prompts,
        "existing_prompts": existing_prompts,
        "missing_prompts": missing_prompts,
    }
