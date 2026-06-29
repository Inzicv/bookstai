"""Context builder agent for BookstAI."""

from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Any

from ..core.errors import InvalidSpoilerLevelError, InvalidWorkflowError
from ..memory.reader import MemoryReader


class ContextBuilder:
    """Build a filtered context from a book memory file."""

    VALID_WORKFLOWS = {"review", "song", "visual", "social"}
    VALID_SPOILER_LEVELS = {"none", "light", "full"}

    WORKFLOW_INCLUDE_RULES = {
        "review": {
            "titre",
            "auteur",
            "personnages",
            "tropes",
            "resume",
            "avis",
            "ambiance",
            "song",
        },
        "song": {
            "titre",
            "auteur",
            "personnages",
            "resume",
            "timeline",
            "evenements",
            "scenes",
            "avis",
        },
        "visual": {
            "titre",
            "auteur",
            "personnages",
            "physique",
            "lieux",
            "ambiance",
            "symboles",
            "scenes",
        },
        "social": {
            "titre",
            "auteur",
            "tropes",
            "avis",
            "ambiance",
        },
    }

    SPOILER_EXCLUDE_RULES = {
        "none": {"spoiler", "timeline", "evenements", "fin", "revelation"},
        "light": {"spoiler", "fin", "revelation"},
        "full": set(),
    }

    def __init__(self, memory_root: Path) -> None:
        self.memory_root = Path(memory_root)
        self.reader = MemoryReader()

    def build(
        self,
        book_slug: str,
        workflow_type: str,
        spoiler_level: str,
    ) -> dict[str, Any]:
        self._validate_workflow(workflow_type)
        self._validate_spoiler_level(spoiler_level)

        source_path = self.memory_root / "books" / f"{book_slug}.md"
        sections = self.reader.read_sections(source_path)

        filtered_sections = {
            section_name: content
            for section_name, content in sections.items()
            if self._should_include_section(section_name, workflow_type, spoiler_level)
        }

        return {
            "book_slug": book_slug,
            "workflow_type": workflow_type,
            "spoiler_level": spoiler_level,
            "source_path": str(source_path),
            "sections": filtered_sections,
            "warnings": [],
        }

    def _validate_workflow(self, workflow_type: str) -> None:
        if workflow_type not in self.VALID_WORKFLOWS:
            raise InvalidWorkflowError(f"Invalid workflow: {workflow_type}")

    def _validate_spoiler_level(self, spoiler_level: str) -> None:
        if spoiler_level not in self.VALID_SPOILER_LEVELS:
            raise InvalidSpoilerLevelError(f"Invalid spoiler level: {spoiler_level}")

    def _should_include_section(
        self,
        section_name: str,
        workflow_type: str,
        spoiler_level: str,
    ) -> bool:
        section_name_normalized = self._normalize_text(section_name)
        workflow_tokens = self.WORKFLOW_INCLUDE_RULES[workflow_type]
        spoiler_tokens = self.SPOILER_EXCLUDE_RULES[spoiler_level]

        if not any(token in section_name_normalized for token in workflow_tokens):
            return False

        if any(token in section_name_normalized for token in spoiler_tokens):
            return False

        return True

    def _normalize_text(self, value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value)
        without_accents = "".join(
            character for character in normalized if not unicodedata.combining(character)
        )
        return without_accents.casefold()
