"""Tests for PromptMakerAgent."""

from pathlib import Path

import pytest

from bookstai.agents.prompt_maker import PromptMakerAgent
from bookstai.core.errors import InvalidPromptTypeError, PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_prompt_maker_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Art: {{art_direction}}\nType: {{prompt_type}}",
        encoding="utf-8",
    )

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Prompts générés"),
    )

    result = agent.generate(
        art_direction="Direction artistique validée",
        prompt_type="scene",
    )

    assert result["agent"] == "prompt_maker"
    assert result["prompt_path"] == "agents/prompt_maker.md"
    assert result["prompt_type"] == "scene"
    assert result["response"] == "Prompts générés"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{art_direction}}", encoding="utf-8")

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock prompt"),
    )

    result = agent.generate(
        art_direction="Direction artistique",
        prompt_type="character",
    )

    assert result["response"] == "Mock prompt"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = PromptMakerAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            art_direction="Direction artistique",
            prompt_type="scene",
        )


@pytest.mark.parametrize("prompt_type", ["character", "scene", "thumbnail", "video"])
def test_agent_accepts_supported_prompt_types(tmp_path: Path, prompt_type: str) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Type: {{prompt_type}}", encoding="utf-8")

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        art_direction="Direction artistique",
        prompt_type=prompt_type,
    )

    assert result["prompt_type"] == prompt_type


def test_agent_raises_invalid_prompt_type_error(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Type: {{prompt_type}}", encoding="utf-8")

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    with pytest.raises(InvalidPromptTypeError):
        agent.generate(
            art_direction="Direction artistique",
            prompt_type="banner",
        )
