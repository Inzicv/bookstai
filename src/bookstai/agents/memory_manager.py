"""Memory manager agent for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from ..prompts.builder import PromptBuilder


class MemoryManagerAgent:
    """Suggest memory updates from generated and corrected content."""

    def __init__(self, prompt_root: Path, llm_client: LLMClient) -> None:
        self.prompt_builder = PromptBuilder(prompt_root=prompt_root)
        self.llm_client = llm_client

    def generate(
        self,
        generated_content: str,
        corrected_content: str,
    ) -> dict[str, str]:
        prompt = self.prompt_builder.build(
            prompt_path="agents/memory_manager.md",
            variables={
                "generated_content": generated_content,
                "corrected_content": corrected_content,
            },
        )
        response = self.llm_client.generate(prompt)

        return {
            "agent": "memory_manager",
            "prompt_path": "agents/memory_manager.md",
            "response": response,
        }
