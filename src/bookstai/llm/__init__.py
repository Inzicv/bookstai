"""LLM client abstractions for BookstAI."""

from .client import LLMClient
from .factory import create_llm_client
from .mock import MockLLMClient

try:  # pragma: no cover - optional dependency
    from .openai_client import OpenAILLMClient
except ImportError:  # pragma: no cover - openai not installed
    OpenAILLMClient = None  # type: ignore[assignment]

__all__ = ["LLMClient", "MockLLMClient", "OpenAILLMClient", "create_llm_client"]
