"""Prompt template renderer for BookstAI."""

from __future__ import annotations

import re
from typing import Any

from ..core.errors import EmptyPromptTemplateError, MissingPromptVariableError


class PromptRenderer:
    """Render raw prompt templates with simple variable replacement."""

    _pattern = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")

    def render(self, template: str, variables: dict[str, Any]) -> str:
        if not template.strip():
            raise EmptyPromptTemplateError("Prompt template is empty")

        def replace(match: re.Match[str]) -> str:
            variable_name = match.group(1)
            if variable_name not in variables:
                raise MissingPromptVariableError(
                    f"Missing prompt variable: {variable_name}"
                )
            return str(variables[variable_name])

        return self._pattern.sub(replace, template)
