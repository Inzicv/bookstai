"""Type definitions for BookstAI."""

from typing import Literal

# Workflow types
WorkflowType = Literal[
    "review",
    "summary",
    "character_analysis",
    "song_generation",
    "visual_design",
]

# Spoiler levels
SpoilerLevel = Literal["none", "low", "medium", "high"]

# LLM Provider types
ProviderType = Literal["openai", "anthropic", "ollama", "mock"]
