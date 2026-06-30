"""Tests for PromptRenderer."""

import pytest

from bookstai.core.errors import (
    EmptyPromptTemplateError,
    MissingPromptVariableError,
)
from bookstai.prompts.renderer import PromptRenderer


def test_render_simple_replacement() -> None:
    renderer = PromptRenderer()

    result = renderer.render(
        template="Livre : {{book_title}}",
        variables={"book_title": "Alchemised"},
    )

    assert result == "Livre : Alchemised"


def test_render_replacement_with_spaces() -> None:
    renderer = PromptRenderer()

    result = renderer.render(
        template="Livre : {{ book_title }}",
        variables={"book_title": "Alchemised"},
    )

    assert result == "Livre : Alchemised"


def test_render_multiple_occurrences_of_same_variable() -> None:
    renderer = PromptRenderer()

    result = renderer.render(
        template="{{name}} / {{ name }} / {{name}}",
        variables={"name": "Book"},
    )

    assert result == "Book / Book / Book"


def test_render_multiple_variables() -> None:
    renderer = PromptRenderer()

    result = renderer.render(
        template="Titre: {{title}}, Auteur: {{ author }}",
        variables={"title": "Alchemised", "author": "SenLinYu"},
    )

    assert result == "Titre: Alchemised, Auteur: SenLinYu"


def test_render_converts_non_string_values() -> None:
    renderer = PromptRenderer()

    result = renderer.render(
        template="Pages: {{pages}}, Score: {{score}}",
        variables={"pages": 432, "score": 4.5},
    )

    assert result == "Pages: 432, Score: 4.5"


def test_render_missing_variable_raises() -> None:
    renderer = PromptRenderer()

    with pytest.raises(MissingPromptVariableError):
        renderer.render(
            template="Livre : {{book_title}}",
            variables={},
        )


def test_render_empty_template_raises() -> None:
    renderer = PromptRenderer()

    with pytest.raises(EmptyPromptTemplateError):
        renderer.render(template="", variables={"x": "y"})


def test_render_whitespace_only_template_raises() -> None:
    renderer = PromptRenderer()

    with pytest.raises(EmptyPromptTemplateError):
        renderer.render(template="   \n\t ", variables={"x": "y"})


def test_render_leaves_plain_text_unchanged() -> None:
    renderer = PromptRenderer()

    result = renderer.render(
        template="Texte sans variable.",
        variables={"unused": "value"},
    )

    assert result == "Texte sans variable."
