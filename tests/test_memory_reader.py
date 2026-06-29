"""Tests for MemoryReader."""

import tempfile
from pathlib import Path

import pytest

from bookstai.core.errors import EmptyMemoryFileError, MemoryFileNotFoundError
from bookstai.memory.reader import MemoryReader


class TestMemoryReaderFileValidation:
    """Tests for file validation in MemoryReader."""

    def test_file_not_found(self) -> None:
        """Test that MemoryFileNotFoundError is raised for non-existent files."""
        nonexistent_path = Path("/nonexistent/path/to/file.md")
        reader = MemoryReader()
        with pytest.raises(MemoryFileNotFoundError):
            reader.read_text(nonexistent_path)

    def test_empty_file(self) -> None:
        """Test that EmptyMemoryFileError is raised for empty files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            with pytest.raises(EmptyMemoryFileError):
                reader.read_text(temp_path)
        finally:
            temp_path.unlink()


class TestMemoryReaderBasicReading:
    """Tests for basic file reading functionality."""

    def test_read_text(self) -> None:
        """Test reading plain text from a file."""
        content = "# Header\nContent here"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            text = reader.read_text(temp_path)
            assert text == content
            assert "# Header" in text
            assert "Content here" in text
        finally:
            temp_path.unlink()

    def test_read_simple_file(self) -> None:
        """Test reading and parsing a simple file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Header\nContent here")
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)
            assert "Header" in sections
        finally:
            temp_path.unlink()


class TestMemoryReaderSectionParsing:
    """Tests for Markdown section parsing."""

    def test_single_section(self) -> None:
        """Test parsing a file with a single section."""
        content = """# Introduction
This is the introduction content."""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            assert len(sections) == 1
            assert "Introduction" in sections
            assert "This is the introduction content." in sections["Introduction"]
        finally:
            temp_path.unlink()

    def test_multiple_sections(self) -> None:
        """Test parsing a file with multiple sections."""
        content = """# Section 1
Content 1

# Section 2
Content 2

# Section 3
Content 3"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            assert len(sections) == 3
            assert "Section 1" in sections
            assert "Section 2" in sections
            assert "Section 3" in sections
            assert "Content 1" in sections["Section 1"]
            assert "Content 2" in sections["Section 2"]
            assert "Content 3" in sections["Section 3"]
        finally:
            temp_path.unlink()

    def test_nested_headers(self) -> None:
        """Test parsing with nested headers (different levels)."""
        content = """# Main Section
Content before subsection

Some more intro text

## Subsection 1
Subsection content

### Sub-subsection
Nested content

## Subsection 2
More content"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            assert "Main Section" in sections
            assert "Subsection 1" in sections
            assert "Sub-subsection" in sections
            assert "Subsection 2" in sections

            # Verify nested content is preserved
            assert "Subsection content" in sections["Subsection 1"]
            assert "Nested content" in sections["Sub-subsection"]
        finally:
            temp_path.unlink()


class TestMemoryReaderPreamble:
    """Tests for preamble (content before first header)."""

    def test_text_before_first_header(self) -> None:
        """Test that text before the first header is stored in 'document' section."""
        content = """This is preamble text.
It can span multiple lines.

# First Section
Content of first section"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            assert "document" in sections
            assert "This is preamble text." in sections["document"]
            assert "It can span multiple lines." in sections["document"]
            assert "First Section" in sections
        finally:
            temp_path.unlink()

    def test_no_preamble(self) -> None:
        """Test that 'document' section is not created if there's no preamble."""
        content = """# First Section
Content"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            assert "document" not in sections
            assert "First Section" in sections
        finally:
            temp_path.unlink()


class TestMemoryReaderPathTypes:
    """Tests for different path types (str and Path)."""

    def test_read_text_with_string_path(self) -> None:
        """Test that read_text accepts string paths."""
        content = "# Header\nContent"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            # Pass as string instead of Path
            text = reader.read_text(str(temp_path))
            assert text == content
        finally:
            temp_path.unlink()

    def test_read_sections_with_string_path(self) -> None:
        """Test that read_sections accepts string paths."""
        content = "# Header\nContent"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            # Pass as string instead of Path
            sections = reader.read_sections(str(temp_path))
            assert "Header" in sections
        finally:
            temp_path.unlink()

    def test_read_text_with_path_object(self) -> None:
        """Test that read_text accepts Path objects."""
        content = "# Header\nContent"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            # Pass as Path object
            text = reader.read_text(temp_path)
            assert text == content
        finally:
            temp_path.unlink()

    def test_read_sections_with_path_object(self) -> None:
        """Test that read_sections accepts Path objects."""
        content = "# Header\nContent"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            # Pass as Path object
            sections = reader.read_sections(temp_path)
            assert "Header" in sections
        finally:
            temp_path.unlink()


class TestMemoryReaderComplexScenarios:
    """Tests for complex real-world scenarios."""

    def test_complex_document(self) -> None:
        """Test parsing a complex document with various structures."""
        content = """# Title
Introduction paragraph

Some more intro text

## Characters
- Character 1
- Character 2

### Main Character
Details about main character

## Plot Summary
Plot details

# Themes
### Theme 1
Discussion

### Theme 2
Discussion

# Reviews
Positive review"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            # Verify all major sections are present
            assert "Title" in sections
            assert "Characters" in sections
            assert "Main Character" in sections
            assert "Plot Summary" in sections
            assert "Themes" in sections
            assert "Theme 1" in sections
            assert "Theme 2" in sections
            assert "Reviews" in sections

            # Verify content is preserved
            assert "Introduction" in sections["Title"]
            assert "Character 1" in sections["Characters"]
        finally:
            temp_path.unlink()

    def test_whitespace_handling(self) -> None:
        """Test handling of various whitespace scenarios."""
        content = """  # Title with leading spaces
Content

#No space after hash
Should not be parsed as header

# Normal Header
Content"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader()
            sections = reader.read_sections(temp_path)

            # Headers should be properly identified
            assert "Title with leading spaces" in sections
        finally:
            temp_path.unlink()
