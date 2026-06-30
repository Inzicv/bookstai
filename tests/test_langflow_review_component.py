"""Tests for the Langflow review adapter."""

from pathlib import Path

from bookstai.langflow.review_component import run_review_workflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_run_review_workflow_returns_complete_result(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    result = run_review_workflow(
        book_slug="example",
        user_opinion="J'ai aimé l'ambiance et les personnages.",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
    )

    assert isinstance(result, dict)
    assert result["workflow"] == "review"
    assert result["book_slug"] == "example"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "review" in result
    assert "social" in result
    assert result["social"]["platform"] == "tiktok"


def test_run_review_workflow_uses_factory_and_transmits_configuration(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["memory_root"] = memory_root
            captured["prompt_root"] = prompt_root
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "review", "book_slug": kwargs["book_slug"]}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["factory"] = {
            "provider": provider,
            "model": model,
            "temperature": temperature,
        }
        return {"provider": provider, "model": model, "temperature": temperature}

    monkeypatch.setattr("bookstai.langflow.review_component.ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr("bookstai.langflow.review_component.create_llm_client", fake_create_llm_client)

    result = run_review_workflow(
        book_slug="example",
        user_opinion="J'ai aimé l'ambiance et les personnages.",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
        provider="openai",
        model="gpt-4o-mini",
        temperature=0.3,
    )

    assert result["workflow"] == "review"
    assert captured["factory"] == {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.3,
    }
    assert captured["llm_client"] == {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.3,
    }
    assert captured["run"] == {
        "book_slug": "example",
        "user_opinion": "J'ai aimé l'ambiance et les personnages.",
        "platform": "tiktok",
    }


def test_run_review_workflow_defaults_to_mock(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            return {"workflow": "review", "book_slug": kwargs["book_slug"]}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["factory"] = {
            "provider": provider,
            "model": model,
            "temperature": temperature,
        }
        return "mock-client"

    monkeypatch.setattr("bookstai.langflow.review_component.ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr("bookstai.langflow.review_component.create_llm_client", fake_create_llm_client)

    run_review_workflow(
        book_slug="example",
        user_opinion="J'ai aimé l'ambiance et les personnages.",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
    )

    assert captured["factory"] == {
        "provider": "mock",
        "model": "gpt-4o-mini",
        "temperature": 0.7,
    }


def test_run_review_workflow_accepts_hitl_and_calls_run_with_hitl(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            pass

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "review"}

        def run_with_hitl(self, **kwargs):
            captured["run_with_hitl"] = kwargs
            return {"workflow": "review", "hitl": {"workflow_name": "review"}}

    monkeypatch.setattr("bookstai.langflow.review_component.ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr("bookstai.langflow.review_component.create_llm_client", lambda **kwargs: "mock-client")

    result = run_review_workflow(
        book_slug="example",
        user_opinion="J'ai aimé",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
        hitl="true",
    )

    assert "run" not in captured
    assert captured["run_with_hitl"] == {
        "book_slug": "example",
        "user_opinion": "J'ai aimé",
        "platform": "tiktok",
    }
    assert result["hitl"]["workflow_name"] == "review"
def test_run_review_workflow_hitl_defaults_to_false(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            pass

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "review"}

        def run_with_hitl(self, **kwargs):
            captured["run_with_hitl"] = kwargs
            return {"workflow": "review", "hitl": {"workflow_name": "review"}}

    monkeypatch.setattr("bookstai.langflow.review_component.ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr("bookstai.langflow.review_component.create_llm_client", lambda **kwargs: "mock-client")

    run_review_workflow(
        book_slug="example",
        user_opinion="J'ai aimÃ©",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
    )

    assert captured["run"] == {
        "book_slug": "example",
        "user_opinion": "J'ai aimÃ©",
        "platform": "tiktok",
    }
    assert "run_with_hitl" not in captured
