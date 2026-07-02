from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from bookstai.api.main import create_app


def _prepare_workspace(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory" / "books"
    memory_root.mkdir(parents=True, exist_ok=True)
    (memory_root / "alchemised.md").write_text("# Book", encoding="utf-8")
    style_root = tmp_path / "memory" / "visual_style" / "Prompts_visuels"
    style_root.mkdir(parents=True, exist_ok=True)
    (style_root / "lego.md").write_text("# Lego\nInstructions de style", encoding="utf-8")
    prompt_root = tmp_path / "prompts"
    (prompt_root / "agents").mkdir(parents=True, exist_ok=True)
    (prompt_root / "agents" / "art_director.md").write_text("Art: {{validated_song}}", encoding="utf-8")
    (prompt_root / "agents" / "prompt_maker.md").write_text("Prompt: {{storyboard}}", encoding="utf-8")


def test_image_storyboard_uses_storyboard_provider_fields(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/image/storyboard",
        json={
            "book_slug": "alchemised",
            "lyrics": "Paroles",
            "visual_style_id": "lego",
            "storyboard_provider": "mock",
            "storyboard_model": None,
            "storyboard_temperature": 0.7,
        },
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_image_generate_batch_uses_image_backend_model_and_quality(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    client = TestClient(create_app())

    response = client.post(
        "/image/generate-batch",
        json={
            "item_slug": "mockingbird-lego-test",
            "image_backend": "mock",
            "image_model": "gpt-image-2",
            "image_quality": "high",
            "storyboard": {"scenes": [{"scene_id": "scene_001", "status": "approved"}]},
            "character_prompts": [{"prompt_id": "character_001", "status": "approved"}],
            "background_prompts": [{"prompt_id": "background_001", "status": "approved"}],
            "confirm_generation": True,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["model"] == "gpt-image-2"
    assert body["quality"] == "high"


def test_image_generate_batch_requires_confirmation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/image/generate-batch",
        json={
            "item_slug": "mockingbird-lego-test",
            "image_backend": "mock",
            "storyboard": {"scenes": [{"scene_id": "scene_001", "status": "approved"}]},
            "character_prompts": [{"prompt_id": "character_001", "status": "approved"}],
            "background_prompts": [{"prompt_id": "background_001", "status": "approved"}],
            "confirm_generation": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["error"]["code"] == "GENERATION_NOT_CONFIRMED"
