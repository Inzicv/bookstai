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


class PromptFileNotFoundError(BookstAIError):
    """Raised when a prompt file cannot be found."""

    pass


class EmptyPromptFileError(BookstAIError):
    """Raised when a prompt file exists but is empty."""

    pass


class MissingPromptVariableError(BookstAIError):
    """Raised when a prompt template variable is missing."""

    pass


class EmptyPromptTemplateError(BookstAIError):
    """Raised when a prompt template is empty."""

    pass
