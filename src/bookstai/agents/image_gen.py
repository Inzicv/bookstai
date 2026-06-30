"""Image generation agent for BookstAI."""

from __future__ import annotations

from ..image.backend import ImageBackend


class ImageGenAgent:
    """Delegate image generation to an injected backend."""

    def __init__(self, backend: ImageBackend) -> None:
        self.backend = backend

    def generate(self, prompt: str) -> dict[str, str]:
        image_path = self.backend.generate(prompt)
        backend_name = getattr(self.backend, "__class__").__name__
        if backend_name == "MockImageBackend":
            backend_label = "mock"
        else:
            backend_label = backend_name

        return {
            "agent": "image_gen",
            "backend": backend_label,
            "image_path": image_path,
        }
