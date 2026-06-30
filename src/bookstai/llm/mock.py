"""Mock LLM client for local development and tests."""

from bookstai.core.errors import EmptyPromptError

DEFAULT_RESPONSE = "Mock response"


class MockLLMClient:
    def __init__(self, response: str = DEFAULT_RESPONSE) -> None:
        self._response = response

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise EmptyPromptError("Prompt must not be empty.")
        return self._response
