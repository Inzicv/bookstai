"""Tests for PromptMakerAgent."""

from pathlib import Path

import pytest

from bookstai.agents.prompt_maker import PromptMakerAgent
from bookstai.core.errors import PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_prompt_maker_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(
        "Storyboard: {{storyboard}}",
        encoding="utf-8",
    )

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Prompts générés"),
    )

    result = agent.generate(
        validated_storyboard="Direction storyboard validée",
        book_context={"book_slug": "alchemised"},
    )

    assert result["agent"] == "prompt_maker"
    assert result["prompt_path"] == "agents/prompt_maker.md"
    assert result["response"] == "Prompts générés"
    assert result["book_context"] == {"book_slug": "alchemised"}
    assert "character_prompts" in result
    assert "background_prompts" in result
    assert "prop_prompts" in result


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text("Prompt: {{storyboard}}", encoding="utf-8")

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock prompt"),
    )

    result = agent.generate(
        validated_storyboard={"shots": []},
        book_context={"book_slug": "alchemised"},
    )

    assert result["response"] == "Mock prompt"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = PromptMakerAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            validated_storyboard="Direction storyboard",
        )


def test_agent_accepts_validated_storyboard(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "prompt_maker.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text("Storyboard: {{storyboard}}", encoding="utf-8")

    agent = PromptMakerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        validated_storyboard={
            "shots": [
                {
                    "shot_number": 1,
                    "characters": ["Astrid"],
                    "background": "Cachots d'Uscaria",
                    "entry_image_idea": "Couloir sombre",
                    "exit_image_idea": "Gros plan sur Astrid",
                }
            ]
        },
        book_context={"book_slug": "alchemised"},
    )

    assert result["response"] == "OK"
