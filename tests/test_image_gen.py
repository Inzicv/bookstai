"""Tests for ImageGenAgent."""

from bookstai.agents.image_gen import ImageGenAgent
from bookstai.image.mock_backend import MockImageBackend


def test_agent_calls_backend() -> None:
    backend = MockImageBackend(image_path="output/mock/image.png")
    agent = ImageGenAgent(backend=backend)

    result = agent.generate(prompt="A fantasy castle at sunset.")

    assert backend.last_prompt == "A fantasy castle at sunset."
    assert result == {
        "agent": "image_gen",
        "backend": "mock",
        "image_path": "output/mock/image.png",
    }


def test_agent_propagates_backend_error() -> None:
    class FailingBackend:
        def generate(self, prompt: str) -> str:
            raise RuntimeError("backend failure")

    agent = ImageGenAgent(backend=FailingBackend())

    try:
        agent.generate(prompt="A fantasy castle at sunset.")
    except RuntimeError as exc:
        assert str(exc) == "backend failure"
    else:
        raise AssertionError("RuntimeError was not raised")
