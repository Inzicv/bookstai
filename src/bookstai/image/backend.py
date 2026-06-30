"""Image backend protocol."""

from typing import Protocol


class ImageBackend(Protocol):
    def generate(self, prompt: str) -> str:
        ...
