from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from bookstai.api.main import create_app


def _write_prompt(prompt_root: Path, name: str, content: str) -> None:
    path = prompt_root / "agents" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _prepare_workspace(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory" / "books"
    memory_root.mkdir(parents=True, exist_ok=True)
    (memory_root / "alchemised.md").write_text("# Book", encoding="utf-8")
    prompt_root = tmp_path / "prompts"
    _write_prompt(prompt_root, "comedy_room.md", "Comedy: {{book_context}}")
    _write_prompt(prompt_root, "review_writer.md", "Review: {{comedy_bank}}")
    _write_prompt(prompt_root, "social_media.md", "Social: {{validated_content}}")
    _write_prompt(prompt_root, "song_writer.md", "Song: {{comedy_bank}}")
    _write_prompt(prompt_root, "art_director.md", "Art: {{validated_song}}")
    _write_prompt(prompt_root, "prompt_maker.md", "Image prompt: {{storyboard}}")


def test_health_route(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "BookstAI", "mode": "local"}


def test_review_run_mock_creates_hitl_session(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimé.",
            "platform": "tiktok",
            "provider": "mock",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": True,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True, body
    assert body["type"] == "review"
    assert body["provider"] == "mock"
    assert body["hitl_enabled"] is True
    assert body["hitl_session_path"] == "outputs/hitl/review/alchemised.json"


def test_review_run_defaults_to_mock_provider(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimÃ©.",
            "platform": "tiktok",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["provider"] == "mock"


def test_review_run_accepts_openai_provider_without_api_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = TestClient(create_app())

    response = client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimÃ©.",
            "platform": "tiktok",
            "provider": "openai",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["error"]["code"] == "MISSING_API_KEY"


def test_review_run_reports_missing_openai_dependency(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from bookstai.api.routes import review as review_routes

    def fake_create_llm_client(**kwargs):
        raise ImportError("missing openai")

    monkeypatch.setattr(review_routes, "create_llm_client", fake_create_llm_client)
    client = TestClient(create_app())

    response = client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimÃ©.",
            "platform": "tiktok",
            "provider": "openai",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["error"]["code"] == "OPENAI_DEPENDENCY_MISSING"


def test_song_run_mock(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/song/run",
        json={
            "book_slug": "alchemised",
            "story_scope": "pitch_only",
            "song_style": "parody",
            "platform": "tiktok",
            "provider": "mock",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": True,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True, body
    assert body["type"] == "song"
    assert body["provider"] == "mock"
    assert body["story_scope"] == "pitch_only"
    assert body["song_style"] == "parody"
    assert "reference_song" not in body
    assert body["hitl_session_path"] == "outputs/hitl/song/alchemised.json"
    assert "image_backend" not in body
    assert "image" not in body["result"]
    assert "storyboard" in body["result"]
    assert "prompts" in body["result"]


def test_song_run_defaults_to_mock_provider(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/song/run",
        json={
            "book_slug": "alchemised",
            "story_scope": "pitch_only",
            "song_style": "parody",
            "platform": "tiktok",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["provider"] == "mock"


def test_song_run_accepts_openai_provider_without_api_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = TestClient(create_app())

    response = client.post(
        "/song/run",
        json={
            "book_slug": "alchemised",
            "story_scope": "pitch_only",
            "song_style": "parody",
            "platform": "tiktok",
            "provider": "openai",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["error"]["code"] == "MISSING_API_KEY"


def test_song_run_reports_missing_openai_dependency(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from bookstai.api.routes import song as song_routes

    def fake_create_llm_client(**kwargs):
        raise ImportError("missing openai")

    monkeypatch.setattr(song_routes, "create_llm_client", fake_create_llm_client)
    client = TestClient(create_app())

    response = client.post(
        "/song/run",
        json={
            "book_slug": "alchemised",
            "story_scope": "pitch_only",
            "song_style": "parody",
            "platform": "tiktok",
            "provider": "openai",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["error"]["code"] == "OPENAI_DEPENDENCY_MISSING"


def test_song_run_mock_full_spoilers(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/song/run",
        json={
            "book_slug": "alchemised",
            "story_scope": "full_spoilers",
            "song_style": "parody",
            "platform": "tiktok",
            "provider": "mock",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["story_scope"] == "full_spoilers"
    assert "reference_song" not in body
    assert body["hitl_session_path"] is None
    assert "image" not in body["result"]


def test_hitl_session_can_be_created_read_and_approved(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimé.",
            "platform": "tiktok",
            "provider": "mock",
            "hitl_enabled": True,
        },
    )

    session = client.get("/hitl/session", params={"type": "review", "book_slug": "alchemised"})
    assert session.status_code == 200
    assert session.json()["session"]["workflow_name"] == "review"

    approve = client.post(
        "/hitl/approve",
        json={
            "type": "review",
            "book_slug": "alchemised",
            "step_id": "comedy",
            "comment": "OK",
        },
    )
    assert approve.status_code == 200
    assert approve.json()["session"]["steps"][0]["status"] == "approved"


def test_learning_apply_refuses_without_confirm(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/learning/apply",
        json={
            "draft_path": "outputs/learning/example.md",
            "confirm": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["error"]["code"] == "CONFIRMATION_REQUIRED"
