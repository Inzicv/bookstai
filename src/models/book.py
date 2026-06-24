"""Module defining the Pydantic models for book extraction."""

from pydantic import BaseModel, Field


class BookMemory(BaseModel):
    """Represents the structured memory/metadata extracted from a book."""

    title: str = Field(
        description="The title of the book, extracted cleanly."
    )
    author: str = Field(
        description="The author of the book."
    )
    summary: str = Field(
        description="A concise summary of the book's plot and content."
    )
    physical_descriptions: list[str] = Field(
        default_factory=list,
        description="List of notable physical descriptions of main characters."
    )
    characters: list[str] = Field(
        default_factory=list,
        description="List of characters along with their brief description or role if possible."
    )
    tropes: list[str] = Field(
        default_factory=list,
        description="List of tropes identified in the book (e.g., enemies-to-lovers, chosen one)."
    )
    themes: list[str] = Field(
        default_factory=list,
        description="List of main themes explored in the book (e.g., love, betrayal, redemption)."
    )
    timeline: list[str] = Field(
        default_factory=list,
        description="List of major story events in chronological order."
    )
    important_scenes: list[str] = Field(
        default_factory=list,
        description="List of the most important scenes or turning points."
    )
    quotes: list[str] = Field(
        default_factory=list,
        description="List of significant or memorable quotes from the book."
    )
