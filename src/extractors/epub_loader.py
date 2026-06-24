"""Module for loading and extracting plain text from EPUB files."""

import warnings
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def load_epub(path: str) -> str:
    """Loads an EPUB file and extracts all text content, stripping HTML tags.

    Args:
        path: Path to the EPUB file.

    Returns:
        The extracted raw text content of the book.
    """
    # Suppress ebooklib user warnings during reading
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        book = epub.read_epub(path)

    text_content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html_content = item.get_content()
            soup = BeautifulSoup(html_content, "html.parser")
            # Extract text using a newline separator for layout readability
            text = soup.get_text(separator="\n")
            # Clean up white space line by line
            lines = [line.strip() for line in text.splitlines()]
            cleaned_text = "\n".join(line for line in lines if line)
            if cleaned_text:
                text_content.append(cleaned_text)

    if not text_content:
        raise ValueError(f"No text content could be extracted from the EPUB at: {path}")

    return "\n\n".join(text_content)
