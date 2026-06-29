"""Custom exceptions for BookstAI."""


class BookstAIError(Exception):
    """Base exception for BookstAI."""

    pass


class MemoryFileNotFoundError(BookstAIError):
    """Raised when a memory file is not found."""

    pass


class InvalidWorkflowError(BookstAIError):
    """Raised when an invalid workflow is used."""

    pass


class InvalidSpoilerLevelError(BookstAIError):
    """Raised when an invalid spoiler level is specified."""

    pass


class EmptyMemoryFileError(BookstAIError):
    """Raised when a memory file is empty."""

    pass
