"""Configuration management for BookstAI."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .types import ProviderType


@dataclass
class BookstAISettings:
    """BookstAI configuration settings."""

    memory_root: Path
    output_root: Path
    provider: ProviderType = "mock"
    model: str = "gpt-4"
    temperature: float = 0.7

    def __post_init__(self) -> None:
        """Validate settings after initialization."""
        if not isinstance(self.memory_root, Path):
            self.memory_root = Path(self.memory_root)
        if not isinstance(self.output_root, Path):
            self.output_root = Path(self.output_root)

        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError(
                f"temperature must be between 0.0 and 2.0, got {self.temperature}"
            )

        if self.provider not in ["openai", "anthropic", "ollama", "mock"]:
            raise ValueError(f"Invalid provider: {self.provider}")


def load_settings(
    memory_root: Optional[str] = None,
    output_root: Optional[str] = None,
    provider: Optional[ProviderType] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> BookstAISettings:
    """
    Load BookstAI settings from environment variables or parameters.

    Environment variables:
        - BOOKSTAI_MEMORY_ROOT: Path to memory files
        - BOOKSTAI_OUTPUT_ROOT: Path to output files
        - BOOKSTAI_PROVIDER: LLM provider (default: mock)
        - BOOKSTAI_MODEL: Model name (default: gpt-4)
        - BOOKSTAI_TEMPERATURE: Temperature (default: 0.7)

    Args:
        memory_root: Memory root path (overrides env var)
        output_root: Output root path (overrides env var)
        provider: LLM provider (overrides env var)
        model: Model name (overrides env var)
        temperature: Temperature (overrides env var)

    Returns:
        BookstAISettings instance

    Raises:
        ValueError: If required settings are missing or invalid
    """
    # Use parameters if provided, otherwise fall back to environment variables
    memory_root = memory_root or os.getenv("BOOKSTAI_MEMORY_ROOT", "./memory")
    output_root = output_root or os.getenv("BOOKSTAI_OUTPUT_ROOT", "./output")
    provider = provider or os.getenv("BOOKSTAI_PROVIDER", "mock")  # type: ignore
    model = model or os.getenv("BOOKSTAI_MODEL", "gpt-4")
    temperature = (
        temperature
        if temperature is not None
        else float(os.getenv("BOOKSTAI_TEMPERATURE", "0.7"))
    )

    return BookstAISettings(
        memory_root=Path(memory_root),
        output_root=Path(output_root),
        provider=provider,  # type: ignore
        model=model,
        temperature=temperature,
    )
