"""Tests for MemoryManagerAgent."""

from pathlib import Path

import pytest

from bookstai.agents.memory_manager import MemoryManagerAgent
from bookstai.core.errors import PromptFileNotFoundError
from bookstai.llm.mock import MockLLMClient


def test_agent_loads_memory_manager_prompt(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "memory_manager.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text(
        "Generated: {{generated_content}}\nCorrected: {{corrected_content}}",
        encoding="utf-8",
    )

    agent = MemoryManagerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Suggestion mémoire"),
    )

    result = agent.generate(
        generated_content="Version IA",
        corrected_content="Version corrigée par Céline",
    )

    assert result["agent"] == "memory_manager"
    assert result["prompt_path"] == "agents/memory_manager.md"
    assert result["response"] == "Suggestion mémoire"


def test_agent_calls_llm_mock(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "memory_manager.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{generated_content}}", encoding="utf-8")

    agent = MemoryManagerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="Mock suggestion"),
    )

    result = agent.generate(
        generated_content="Version IA",
        corrected_content="Version corrigée",
    )

    assert result["response"] == "Mock suggestion"


def test_agent_propagates_missing_prompt_error(tmp_path: Path) -> None:
    agent = MemoryManagerAgent(
        prompt_root=tmp_path / "prompts",
        llm_client=MockLLMClient(response="unused"),
    )

    with pytest.raises(PromptFileNotFoundError):
        agent.generate(
            generated_content="Version IA",
            corrected_content="Version corrigée",
        )


def test_agent_accepts_generated_content_string(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "memory_manager.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Generated: {{generated_content}}", encoding="utf-8")

    agent = MemoryManagerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        generated_content="Version IA",
        corrected_content="Version corrigée",
    )

    assert result["response"] == "OK"


def test_agent_accepts_corrected_content_string(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "memory_manager.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Corrected: {{corrected_content}}", encoding="utf-8")

    agent = MemoryManagerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    result = agent.generate(
        generated_content="Version IA",
        corrected_content="Version corrigée",
    )

    assert result["response"] == "OK"


def test_agent_does_not_write_memory_files(tmp_path: Path) -> None:
    prompt_root = tmp_path / "prompts"
    prompt_file = prompt_root / "agents" / "memory_manager.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Prompt: {{generated_content}}", encoding="utf-8")

    memory_root = tmp_path / "memory"
    memory_root.mkdir()

    agent = MemoryManagerAgent(
        prompt_root=prompt_root,
        llm_client=MockLLMClient(response="OK"),
    )

    agent.generate(
        generated_content="Version IA",
        corrected_content="Version corrigée",
    )

    assert list(memory_root.rglob("*")) == []
