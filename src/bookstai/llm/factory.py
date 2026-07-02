"""Factory helpers for BookstAI LLM clients."""

from __future__ import annotations

from ..core.errors import UnsupportedProviderError
from ..core.types import ProviderType
from .client import LLMClient
from .mock import MockLLMClient

try:  # pragma: no cover - optional dependency
    from .openai_client import OpenAILLMClient
except ImportError:  # pragma: no cover - openai not installed
    OpenAILLMClient = None  # type: ignore[assignment]


def create_llm_client(
    provider: ProviderType = "mock",
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> LLMClient:
    if provider == "mock":
        return MockLLMClient()
    if provider == "openai":
        if OpenAILLMClient is None:
            raise ImportError(
                "The 'openai' package is required to create an OpenAILLMClient."
            )
        return OpenAILLMClient(model=model)
    if provider in {"anthropic", "ollama"}:
        raise UnsupportedProviderError(f"Provider '{provider}' is not supported yet.")
    raise UnsupportedProviderError(f"Provider '{provider}' is not supported yet.")
