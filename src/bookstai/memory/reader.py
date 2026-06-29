"""Memory file reader for BookstAI."""

import re
from pathlib import Path
from typing import Dict, Optional

from ..core.errors import (
    EmptyMemoryFileError,
    MemoryFileNotFoundError,
)


class MemoryReader:
    """
    Reads and parses Markdown memory files.

    A MemoryReader can:
    - Verify that a file exists
    - Verify that a file is not empty
    - Parse Markdown sections (headers: #, ##, ###, etc.)
    - Return a dictionary {section_name: section_content}
    - Preserve text before the first header in a "document" section
    """

    def __init__(self, file_path: Path) -> None:
        """
        Initialize MemoryReader with a file path.

        Args:
            file_path: Path to the Markdown file

        Raises:
            MemoryFileNotFoundError: If the file does not exist
            EmptyMemoryFileError: If the file is empty
        """
        self.file_path = Path(file_path)
        self._validate_file()
        self._content = self._read_file()
        self._sections: Optional[Dict[str, str]] = None

    def _validate_file(self) -> None:
        """
        Validate that the file exists and is not empty.

        Raises:
            MemoryFileNotFoundError: If the file does not exist
            EmptyMemoryFileError: If the file is empty
        """
        if not self.file_path.exists():
            raise MemoryFileNotFoundError(
                f"Memory file not found: {self.file_path}"
            )

        if self.file_path.stat().st_size == 0:
            raise EmptyMemoryFileError(f"Memory file is empty: {self.file_path}")

    def _read_file(self) -> str:
        """
        Read the file content.

        Returns:
            The file content as a string
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def parse(self) -> Dict[str, str]:
        """
        Parse the Markdown file into sections.

        Returns:
            A dictionary where keys are section names and values are section contents.
            Text before the first header is stored in the "document" section.

        Example:
            For a file with content:
            ```
            Some intro text

            # Section 1
            Content 1

            ## Subsection
            Content 2

            # Section 2
            Content 3
            ```

            Returns:
            {
                "document": "Some intro text",
                "Section 1": "Content 1\n\n## Subsection\nContent 2",
                "Section 2": "Content 3"
            }
        """
        if self._sections is not None:
            return self._sections

        sections: Dict[str, str] = {}
        lines = self._content.split("\n")

        # Pattern to match Markdown headers: # Header, ## Header, etc.
        # Allows optional leading whitespace but requires space after #
        header_pattern = re.compile(r"^\s*(#{1,6})\s+(.+)$")

        current_section: Optional[str] = None
        current_content: list[str] = []
        preamble: list[str] = []

        for line in lines:
            match = header_pattern.match(line)

            if match:
                # Found a header
                # Save previous section if it exists
                if current_section is not None:
                    section_content = "\n".join(current_content).strip()
                    # Save section even if empty (except the "document" section)
                    sections[current_section] = section_content
                elif preamble or current_content:
                    # We haven't found any header yet, this is preamble
                    preamble.extend(current_content)

                # Extract the header text (remove the # symbols)
                header_level = match.group(1)
                header_text = match.group(2).strip()

                # For consistency, we normalize all sections to the same level
                # (we use the header text as the section name)
                current_section = header_text
                current_content = []
            else:
                # Regular content line
                if current_section is not None:
                    current_content.append(line)
                else:
                    preamble.append(line)

        # Save the last section
        if current_section is not None:
            section_content = "\n".join(current_content).strip()
            sections[current_section] = section_content

        # Add preamble if it exists
        preamble_text = "\n".join(preamble).strip()
        if preamble_text:
            sections["document"] = preamble_text

        self._sections = sections
        return sections

    def get_section(self, section_name: str) -> Optional[str]:
        """
        Get the content of a specific section.

        Args:
            section_name: The name of the section

        Returns:
            The section content, or None if the section doesn't exist
        """
        sections = self.parse()
        return sections.get(section_name)

    def get_all_sections(self) -> Dict[str, str]:
        """
        Get all parsed sections.

        Returns:
            A dictionary of all sections
        """
        return self.parse()

    def section_exists(self, section_name: str) -> bool:
        """
        Check if a section exists.

        Args:
            section_name: The name of the section

        Returns:
            True if the section exists, False otherwise
        """
        return section_name in self.parse()

    def get_section_names(self) -> list[str]:
        """
        Get all section names.

        Returns:
            A list of section names
        """
        return list(self.parse().keys())
