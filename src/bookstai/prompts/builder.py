"""Prompt builder for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .loader import PromptLoader
from .renderer import PromptRenderer


class PromptBuilder:
    """Build a final prompt from a Markdown template and variables."""

    def __init__(self, prompt_root: Path) -> None:
        self.loader = PromptLoader(prompt_root=prompt_root)
        self.renderer = PromptRenderer()

    def build(self, prompt_path: str | Path, variables: dict[str, object]) -> str:
        template = self.loader.load(prompt_path)
        return self.renderer.render(template=template, variables=variables)
