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
    InvalidSpoilerModeError,
    InvalidPromptTypeError,
    InvalidPlatformError,
    EmptyMemoryFileError,
    EmptyPromptError,
)
from .core.types import WorkflowType, SpoilerLevel, ProviderType
from .memory.reader import MemoryReader
from .agents.context_builder import ContextBuilder
from .agents.comedy_room import ComedyRoomAgent
from .agents.art_director import ArtDirectorAgent
from .agents.image_gen import ImageGenAgent
from .agents.review_writer import ReviewWriterAgent
from .agents.song_writer import SongWriterAgent
from .agents.prompt_maker import PromptMakerAgent
from .agents.social_media import SocialMediaAgent
from .agents.memory_manager import MemoryManagerAgent
from .agents.style_memory import StyleMemoryAgent
from .image.backend import ImageBackend
from .image.mock_backend import MockImageBackend
from .prompts.builder import PromptBuilder
from .prompts.loader import PromptLoader
from .prompts.renderer import PromptRenderer
from .exports.markdown import MarkdownExporter
from .exports.json import JSONExporter
from .exports.service import ExportService
from .hitl import HITLStatus, HITLStep, HITLSession
from .learning import LearningCandidate, LearningExtraction, LearningExtractor
from .history import HistoryEntry, HistoryStore
from .logging import configure_logging
from .workflows.review import ReviewWorkflow
from .workflows.song import SongWorkflow
from .langflow.review_component import run_review_workflow
from .langflow.song_component import run_song_workflow
from .precheck import REQUIRED_AGENT_PROMPTS, check_required_agent_prompts
from .cli import main

__all__ = [
    "BookstAISettings",
    "load_settings",
    "BookstAIError",
    "MemoryFileNotFoundError",
    "InvalidWorkflowError",
    "InvalidSpoilerLevelError",
    "InvalidSpoilerModeError",
    "InvalidPromptTypeError",
    "InvalidPlatformError",
    "EmptyMemoryFileError",
    "EmptyPromptError",
    "WorkflowType",
    "SpoilerLevel",
    "ProviderType",
    "MemoryReader",
    "ContextBuilder",
    "ComedyRoomAgent",
    "ArtDirectorAgent",
    "ImageGenAgent",
    "ReviewWriterAgent",
    "SongWriterAgent",
    "PromptMakerAgent",
    "SocialMediaAgent",
    "MemoryManagerAgent",
    "StyleMemoryAgent",
    "ImageBackend",
    "MockImageBackend",
    "ReviewWorkflow",
    "SongWorkflow",
    "run_review_workflow",
    "run_song_workflow",
    "REQUIRED_AGENT_PROMPTS",
    "check_required_agent_prompts",
    "MarkdownExporter",
    "JSONExporter",
    "ExportService",
    "HITLStatus",
    "HITLStep",
    "HITLSession",
    "LearningCandidate",
    "LearningExtraction",
    "LearningExtractor",
    "HistoryEntry",
    "HistoryStore",
    "configure_logging",
    "main",
    "PromptBuilder",
    "PromptLoader",
    "PromptRenderer",
]
