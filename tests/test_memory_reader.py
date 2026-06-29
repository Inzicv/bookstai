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
        with pytest.raises(MemoryFileNotFoundError):
            MemoryReader(nonexistent_path)

    def test_empty_file(self) -> None:
        """Test that EmptyMemoryFileError is raised for empty files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = Path(f.name)

        try:
            with pytest.raises(EmptyMemoryFileError):
                MemoryReader(temp_path)
        finally:
            temp_path.unlink()


class TestMemoryReaderBasicReading:
    """Tests for basic file reading functionality."""

    def test_read_simple_file(self) -> None:
        """Test reading a simple file with content."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Header\nContent here")
            temp_path = Path(f.name)

        try:
            reader = MemoryReader(temp_path)
            assert reader.file_path == temp_path
            sections = reader.parse()
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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

            assert "document" not in sections
            assert "First Section" in sections
        finally:
            temp_path.unlink()


class TestMemoryReaderMethods:
    """Tests for helper methods."""

    def test_get_section(self) -> None:
        """Test getting a specific section by name."""
        content = """# Section A
Content A

# Section B
Content B"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader(temp_path)

            assert "Content A" in reader.get_section("Section A")  # type: ignore
            assert "Content B" in reader.get_section("Section B")  # type: ignore
            assert reader.get_section("Non-existent") is None
        finally:
            temp_path.unlink()

    def test_section_exists(self) -> None:
        """Test checking if a section exists."""
        content = """# Existing Section
Content"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader(temp_path)

            assert reader.section_exists("Existing Section")
            assert not reader.section_exists("Non-existent Section")
        finally:
            temp_path.unlink()

    def test_get_section_names(self) -> None:
        """Test getting all section names."""
        content = """Preamble text

# Section 1
Content 1

# Section 2
Content 2"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader(temp_path)
            names = reader.get_section_names()

            assert "document" in names
            assert "Section 1" in names
            assert "Section 2" in names
            assert len(names) == 3
        finally:
            temp_path.unlink()

    def test_get_all_sections(self) -> None:
        """Test getting all sections at once."""
        content = """# Section 1
Content 1

# Section 2
Content 2"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader(temp_path)
            sections = reader.get_all_sections()

            assert isinstance(sections, dict)
            assert len(sections) == 2
            assert "Section 1" in sections
            assert "Section 2" in sections
        finally:
            temp_path.unlink()


class TestMemoryReaderCaching:
    """Tests for caching behavior."""

    def test_parse_caching(self) -> None:
        """Test that parse() results are cached."""
        content = """# Section
Content"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            reader = MemoryReader(temp_path)
            sections1 = reader.parse()
            sections2 = reader.parse()

            # Should return the same object (cached)
            assert sections1 is sections2
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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

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
            reader = MemoryReader(temp_path)
            sections = reader.parse()

            # Headers should be properly identified
            assert "Title with leading spaces" in sections
        finally:
            temp_path.unlink()
