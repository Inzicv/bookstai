"""Tests for SocialMediaAgent."""

from pathlib import Path

import pytest

from bookstai.agents.social_media import SocialMediaAgent
from bookstai.core.errors import InvalidPlatformError, PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_social_media_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "social_media.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Content: {{validated_content}}\nStyle: {{style_context}}\nPlatform: {{platform}}",
        encoding="utf-8",
    )

    agent = SocialMediaAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Caption + hashtags"),
    )

    result = agent.generate(
        validated_content="Review validée ou chanson validée",
        style_context={"reviews": {"examples": "Style Céline"}},
        platform="instagram",
    )

    assert result["agent"] == "social_media"
    assert result["prompt_path"] == "agents/social_media.md"
    assert result["platform"] == "instagram"
    assert result["response"] == "Caption + hashtags"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "social_media.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{validated_content}}", encoding="utf-8")

    agent = SocialMediaAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock social"),
    )

    result = agent.generate(
        validated_content="Texte validé",
        style_context={"a": 1},
        platform="tiktok",
    )

    assert result["response"] == "Mock social"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = SocialMediaAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            validated_content="Texte validé",
            style_context={},
            platform="instagram",
        )


@pytest.mark.parametrize("platform", ["instagram", "tiktok", "youtube_shorts"])
def test_agent_accepts_supported_platforms(tmp_path: Path, platform: str) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "social_media.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Platform: {{platform}}", encoding="utf-8")

    agent = SocialMediaAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        validated_content="Texte validé",
        style_context={"social": True},
        platform=platform,
    )

    assert result["platform"] == platform


def test_agent_raises_invalid_platform_error(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "social_media.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Platform: {{platform}}", encoding="utf-8")

    agent = SocialMediaAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    with pytest.raises(InvalidPlatformError):
        agent.generate(
            validated_content="Texte validé",
            style_context={},
            platform="linkedin",
        )
