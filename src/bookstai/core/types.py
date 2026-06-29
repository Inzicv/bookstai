"""Type definitions for BookstAI."""

from typing import Literal

WorkflowType = Literal["review", "song", "visual", "social"]
SpoilerLevel = Literal["none", "light", "full"]
ProviderType = Literal["openai", "anthropic", "ollama", "mock"]