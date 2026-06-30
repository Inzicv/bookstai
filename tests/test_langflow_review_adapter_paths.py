"""Tests for Langflow review adapter path resolution."""

from __future__ import annotations

from pathlib import Path

import bookstai

from bookstai.langflow import review_component


def test_run_review_workflow_resolves_prompt_root_from_package(monkeypatch, tmp_path: Path) -> None:
    package_root = tmp_path / "site-packages" / "bookstai"
    package_root.mkdir(parents=True, exist_ok=True)
    fake_init = package_root / "__init__.py"
    fake_init.write_text("__all__ = []", encoding="utf-8")
    monkeypatch.setattr(bookstai, "__file__", str(fake_init))
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.chdir(workspace)

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["memory_root"] = memory_root
            captured["prompt_root"] = prompt_root
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            return {"workflow": "review"}

    monkeypatch.setattr(review_component, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(review_component, "create_llm_client", lambda **kwargs: "mock-client")
    review_component.run_review_workflow(
        book_slug="example",
        user_opinion="opinion",
        platform="tiktok",
        provider="mock",
    )

    assert captured["prompt_root"] == prompts_dir
    assert captured["memory_root"] == memory_dir
