"""Tests for MockImageBackend."""

from bookstai.image.mock_backend import MockImageBackend
from bookstai.image.types import ImageGenerationRequest


def test_mock_backend_returns_configured_path() -> None:
    backend = MockImageBackend(image_path="outputs/mock/image.png")

    result = backend.generate(ImageGenerationRequest(prompt="A fantasy castle at sunset."))

    assert result.ok is True
    assert result.backend == "mock"
    assert result.image_path == "outputs/mock/image.png"
    assert result.prompt == "A fantasy castle at sunset."


def test_mock_backend_keeps_prompt_and_request() -> None:
    backend = MockImageBackend(image_path="outputs/mock/image.png")
    request = ImageGenerationRequest(prompt="A fantasy castle at sunset.")

    backend.generate(request)

    assert backend.last_prompt == "A fantasy castle at sunset."
    assert backend.last_request == request


def test_mock_backend_healthcheck() -> None:
    backend = MockImageBackend()

    result = backend.healthcheck()

    assert result.ok is True
    assert result.backend == "mock"
    assert result.message == "Mock image backend is available."
