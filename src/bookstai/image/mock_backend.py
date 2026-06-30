"""Mock image backend for BookstAI."""

from __future__ import annotations

from .backend import ImageBackend


class MockImageBackend:
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.last_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.image_path
