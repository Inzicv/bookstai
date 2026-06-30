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
    EmptyPromptError,
)
from .core.types import WorkflowType, SpoilerLevel, ProviderType
from .memory.reader import MemoryReader
from .agents.context_builder import ContextBuilder
from .agents.style_memory import StyleMemoryAgent
from .prompts.builder import PromptBuilder
from .prompts.loader import PromptLoader
from .prompts.renderer import PromptRenderer

__all__ = [
    "BookstAISettings",
    "load_settings",
    "BookstAIError",
    "MemoryFileNotFoundError",
    "InvalidWorkflowError",
    "InvalidSpoilerLevelError",
    "EmptyMemoryFileError",
    "EmptyPromptError",
    "WorkflowType",
    "SpoilerLevel",
    "ProviderType",
    "MemoryReader",
    "ContextBuilder",
    "StyleMemoryAgent",
    "PromptBuilder",
    "PromptLoader",
    "PromptRenderer",
]
