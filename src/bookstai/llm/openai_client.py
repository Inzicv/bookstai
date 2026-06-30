"""OpenAI LLM client for BookstAI."""

from __future__ import annotations

import os
from typing import Any

from ..core.errors import EmptyPromptError, MissingAPIKeyError
from .client import LLMClient


class OpenAILLMClient:
    """OpenAI-backed implementation of the BookstAI LLM interface."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyError(
                "OPENAI_API_KEY is required to use OpenAILLMClient."
            )

        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - exercised when dependency is missing
            raise ImportError(
                "The 'openai' package is required to use OpenAILLMClient."
            ) from exc

        self._client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise EmptyPromptError("Prompt must not be empty.")

        response = self._client.responses.create(
            model=self.model,
            input=prompt,
            temperature=self.temperature,
        )

        output_text = getattr(response, "output_text", None)
        if output_text and output_text.strip():
            return output_text

        text_parts: list[str] = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    if hasattr(text, "value"):
                        text_parts.append(str(text.value))
                    else:
                        text_parts.append(str(text))

        combined_text = "".join(text_parts).strip()
        if combined_text:
            return combined_text

        raise ValueError("OpenAI response did not contain any usable text.")
