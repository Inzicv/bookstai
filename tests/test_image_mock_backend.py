"""Tests for MockImageBackend."""

from bookstai.image.mock_backend import MockImageBackend


def test_mock_backend_returns_configured_path() -> None:
    backend = MockImageBackend(image_path="output/mock/image.png")

    assert backend.generate("A fantasy castle at sunset.") == "output/mock/image.png"


def test_mock_backend_keeps_prompt() -> None:
    backend = MockImageBackend(image_path="output/mock/image.png")

    backend.generate("A fantasy castle at sunset.")

    assert backend.last_prompt == "A fantasy castle at sunset."
