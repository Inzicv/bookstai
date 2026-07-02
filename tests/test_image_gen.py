"""Tests for ImageGenAgent."""

from bookstai.agents.image_gen import ImageGenAgent
from bookstai.image.mock_backend import MockImageBackend
from bookstai.image.types import ImageGenerationRequest


def test_agent_calls_backend() -> None:
    backend = MockImageBackend(image_path="output/mock/image.png")
    agent = ImageGenAgent(backend=backend)
    request = ImageGenerationRequest(prompt="A fantasy castle at sunset.")

    result = agent.generate(request=request)

    assert backend.last_prompt == "A fantasy castle at sunset."
    assert result.ok is True
    assert result.backend == "mock"
    assert result.image_path == "output/mock/image.png"


def test_agent_propagates_backend_error() -> None:
    class FailingBackend:
        def generate(self, request: ImageGenerationRequest):
            raise RuntimeError("backend failure")

    agent = ImageGenAgent(backend=FailingBackend())

    try:
        agent.generate(request=ImageGenerationRequest(prompt="A fantasy castle at sunset."))
    except RuntimeError as exc:
        assert str(exc) == "backend failure"
    else:
        raise AssertionError("RuntimeError was not raised")
