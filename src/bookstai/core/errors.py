"""Custom exceptions for BookstAI."""


class BookstAIError(Exception):
    """Base exception for BookstAI."""

    pass


class MissingAPIKeyError(BookstAIError):
    """Raised when a required API key is missing."""

    pass


class UnsupportedProviderError(BookstAIError):
    """Raised when a provider is known but not supported yet."""

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


class EmptyPromptError(BookstAIError):
    """Raised when a prompt sent to an LLM is empty."""

    pass


class InvalidSpoilerModeError(BookstAIError):
    """Raised when a song spoiler mode is invalid."""

    pass


class InvalidPromptTypeError(BookstAIError):
    """Raised when an image prompt type is invalid."""

    pass


class InvalidPlatformError(BookstAIError):
    """Raised when a social media platform is invalid."""

    pass


class InvalidExportFormatError(BookstAIError):
    """Raised when an export format is invalid."""

    pass


class ImageBackendError(BookstAIError):
    """Raised when an image backend fails."""

    pass


class ImageGenerationError(ImageBackendError):
    """Raised when image generation fails."""

    pass


class ImageBackendConnectionError(ImageBackendError):
    """Raised when an image backend cannot be reached."""

    pass


class UnsupportedImageBackendError(BookstAIError):
    """Raised when an image backend is not supported."""

    pass
