"""
BookstAI - AI-powered book analysis and content generation framework.
"""

__version__ = "0.1.0"
__author__ = "BookstAI Team"

from .core.config import BookstAISettings, load_settings
from .core.errors import (
    BookstAIError,
    MemoryFileNotFoundError,
    InvalidWorkflowError,
    InvalidSpoilerLevelError,
    EmptyMemoryFileError,
)
from .core.types import WorkflowType, SpoilerLevel, ProviderType
from .memory.reader import MemoryReader
from .agents.context_builder import ContextBuilder
from .prompts.loader import PromptLoader

__all__ = [
    "BookstAISettings",
    "load_settings",
    "BookstAIError",
    "MemoryFileNotFoundError",
    "InvalidWorkflowError",
    "InvalidSpoilerLevelError",
    "EmptyMemoryFileError",
    "WorkflowType",
    "SpoilerLevel",
    "ProviderType",
    "MemoryReader",
    "ContextBuilder",
    "PromptLoader",
]
