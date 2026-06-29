"""Memory file reader for BookstAI."""

import re
from pathlib import Path
from typing import Dict

from ..core.errors import (
    EmptyMemoryFileError,
    MemoryFileNotFoundError,
)


class MemoryReader:
    """
    Reads and parses Markdown memory files.

    A MemoryReader can:
    - Read plain text from a file
    - Verify that a file exists and is not empty
    - Parse Markdown sections (headers: #, ##, ###, etc.)
    - Return a dictionary {section_name: section_content}
    - Preserve text before the first header in a "document" section
    """

    def read_text(self, path: str | Path) -> str:
        """
        Read the plain text content of a file.

        Args:
            path: Path to the file

        Returns:
            The file content as a string

        Raises:
            MemoryFileNotFoundError: If the file does not exist
            EmptyMemoryFileError: If the file is empty
        """
        file_path = Path(path)
        self._validate_file(file_path)
        return self._read_file(file_path)

    def read_sections(self, path: str | Path) -> Dict[str, str]:
        """
        Read and parse a Markdown file into sections.

        Args:
            path: Path to the file

        Returns:
            A dictionary where keys are section names and values are section contents.
            Text before the first header is stored in the "document" section.

        Raises:
            MemoryFileNotFoundError: If the file does not exist
            EmptyMemoryFileError: If the file is empty

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
        file_path = Path(path)
        content = self.read_text(file_path)
        return self._parse_sections(content)

    def _validate_file(self, file_path: Path) -> None:
        """
        Validate that the file exists and is not empty.

        Args:
            file_path: Path to the file to validate

        Raises:
            MemoryFileNotFoundError: If the file does not exist
            EmptyMemoryFileError: If the file is empty
        """
        if not file_path.exists():
            raise MemoryFileNotFoundError(
                f"Memory file not found: {file_path}"
            )

        if file_path.stat().st_size == 0:
            raise EmptyMemoryFileError(f"Memory file is empty: {file_path}")

    def _read_file(self, file_path: Path) -> str:
        """
        Read the file content.

        Args:
            file_path: Path to the file to read

        Returns:
            The file content as a string
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """
        Parse Markdown content into sections.

        Args:
            content: The Markdown content to parse

        Returns:
            A dictionary of sections
        """
        sections: Dict[str, str] = {}
        lines = content.split("\n")

        # Pattern to match Markdown headers: # Header, ## Header, etc.
        # Allows optional leading whitespace but requires space after #
        header_pattern = re.compile(r"^\s*(#{1,6})\s+(.+)$")

        current_section: str | None = None
        current_content: list[str] = []
        preamble: list[str] = []

        for line in lines:
            match = header_pattern.match(line)

            if match:
                # Found a header
                # Save previous section if it exists
                if current_section is not None:
                    section_content = "\n".join(current_content).strip()
                    # Save section even if empty
                    sections[current_section] = section_content
                elif preamble or current_content:
                    # We haven't found any header yet, this is preamble
                    preamble.extend(current_content)

                # Extract the header text (remove the # symbols)
                header_level = match.group(1)
                header_text = match.group(2).strip()

                # Use the header text as the section name
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

        return sections
