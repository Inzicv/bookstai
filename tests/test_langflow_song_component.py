"""Tests for the Langflow song adapter."""

from pathlib import Path

from bookstai.langflow.song_component import run_song_workflow


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    prompt_file = prompt_root / "agents" / name
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(content, encoding="utf-8")


def test_run_song_workflow_returns_complete_result(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    result = run_song_workflow(
        book_slug="example",
        spoiler_mode="spoiler_free",
        prompt_type="thumbnail",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
        image_path=str(tmp_path / "outputs" / "mock" / "image.png"),
    )

    assert isinstance(result, dict)
    assert result["workflow"] == "song"
    assert result["book_slug"] == "example"
    assert "context" in result
    assert "style" in result
    assert "comedy" in result
    assert "song" in result
    assert "art_direction" in result
    assert "image_prompt" in result
    assert "image" in result
    assert "social" in result
    assert result["social"]["platform"] == "tiktok"


def test_run_song_workflow_uses_factory_and_transmits_configuration(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["memory_root"] = memory_root
            captured["prompt_root"] = prompt_root
            captured["llm_client"] = llm_client
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "song", "book_slug": kwargs["book_slug"]}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["llm_factory"] = {
            "provider": provider,
            "model": model,
            "temperature": temperature,
        }
        return {"provider": provider, "model": model, "temperature": temperature}

    def fake_create_image_backend(**kwargs):
        captured["image_factory"] = kwargs
        return {"backend": kwargs["backend"], "image_path": kwargs["image_path"]}

    monkeypatch.setattr("bookstai.langflow.song_component.SongWorkflow", DummyWorkflow)
    monkeypatch.setattr("bookstai.langflow.song_component.create_llm_client", fake_create_llm_client)
    monkeypatch.setattr("bookstai.langflow.song_component.create_image_backend", fake_create_image_backend)

    result = run_song_workflow(
        book_slug="example",
        spoiler_mode="spoiler_free",
        prompt_type="thumbnail",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
        image_path=str(tmp_path / "outputs" / "mock" / "image.png"),
        provider="openai",
        model="gpt-4o-mini",
        temperature=0.4,
        image_backend="comfyui",
        comfyui_url="http://127.0.0.1:8188",
        comfyui_workflow_path=tmp_path / "workflow.json",
        image_output_dir=tmp_path / "outputs" / "images",
        image_timeout=30.0,
        image_poll_interval=0.5,
    )

    assert result["workflow"] == "song"
    assert captured["llm_factory"] == {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.4,
    }
    assert captured["image_factory"]["backend"] == "comfyui"
    assert captured["image_factory"]["image_path"] == str(tmp_path / "outputs" / "mock" / "image.png")
    assert captured["image_factory"]["comfyui_url"] == "http://127.0.0.1:8188"
    assert captured["image_factory"]["workflow_path"] == tmp_path / "workflow.json"
    assert captured["image_factory"]["output_dir"] == tmp_path / "outputs" / "images"
    assert captured["image_factory"]["timeout"] == 30.0
    assert captured["image_factory"]["poll_interval"] == 0.5
    assert captured["image_backend"]["backend"] == "comfyui"
    assert captured["run"] == {
        "book_slug": "example",
        "spoiler_mode": "spoiler_free",
        "prompt_type": "thumbnail",
        "platform": "tiktok",
    }


def test_run_song_workflow_defaults_to_mock(monkeypatch, tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    book_file = memory_root / "books" / "example.md"
    book_file.parent.mkdir(parents=True)
    book_file.write_text("# Example\nA small memory file.", encoding="utf-8")

    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_content}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Prompt: {{art_direction}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")

    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["llm_client"] = llm_client
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            return {"workflow": "song", "book_slug": kwargs["book_slug"]}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["llm_factory"] = {
            "provider": provider,
            "model": model,
            "temperature": temperature,
        }
        return "mock-client"

    def fake_create_image_backend(**kwargs):
        captured["image_factory"] = kwargs
        return "mock-image-backend"

    monkeypatch.setattr("bookstai.langflow.song_component.SongWorkflow", DummyWorkflow)
    monkeypatch.setattr("bookstai.langflow.song_component.create_llm_client", fake_create_llm_client)
    monkeypatch.setattr("bookstai.langflow.song_component.create_image_backend", fake_create_image_backend)

    run_song_workflow(
        book_slug="example",
        spoiler_mode="spoiler_free",
        prompt_type="thumbnail",
        platform="tiktok",
        memory_root=str(memory_root),
        prompt_root=str(prompt_root),
        image_path=str(tmp_path / "outputs" / "mock" / "image.png"),
    )

    assert captured["llm_factory"] == {
        "provider": "mock",
        "model": "gpt-4o-mini",
        "temperature": 0.7,
    }
    assert captured["image_factory"]["backend"] == "mock"
