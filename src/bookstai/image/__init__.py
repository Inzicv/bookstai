"""Image generation abstractions for BookstAI."""

from .backend import ImageBackend
from .mock_backend import MockImageBackend

__all__ = ["ImageBackend", "MockImageBackend"]
