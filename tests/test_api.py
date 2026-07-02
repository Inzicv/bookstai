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
    style_root = tmp_path / "memory" / "visual_style" / "Prompts_visuels"
    style_root.mkdir(parents=True, exist_ok=True)
    (style_root / "lego.md").write_text("# Lego\nInstructions de style", encoding="utf-8")
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


def test_books_list_returns_empty_list_when_folder_is_empty(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    client = TestClient(create_app())

    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "books": []}


def test_books_create_read_update_and_duplicate_validation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    client = TestClient(create_app())

    create = client.post(
        "/books",
        json={
            "title": "Les Héritiers d’Orion",
            "slug": "les-heritiers-d-orion",
            "content": "# Les Héritiers d’Orion\n\nContenu",
        },
    )
    assert create.status_code == 200
    assert create.json()["ok"] is True
    assert (tmp_path / "memory" / "books" / "les-heritiers-d-orion.md").exists()

    read = client.get("/books/les-heritiers-d-orion")
    assert read.status_code == 200
    assert read.json()["book"]["content"].startswith("# Les Héritiers d’Orion")

    duplicate = client.post(
        "/books",
        json={
            "title": "Les Héritiers d’Orion",
            "slug": "les-heritiers-d-orion",
            "content": "# Les Héritiers d’Orion\n\nContenu",
        },
    )
    assert duplicate.status_code == 200
    assert duplicate.json()["error"]["code"] == "BOOK_ALREADY_EXISTS"

    update = client.put(
        "/books/les-heritiers-d-orion",
        json={
            "title": "Les Héritiers d’Orion",
            "content": "# Les Héritiers d’Orion\n\nContenu mis à jour",
        },
    )
    assert update.status_code == 200
    assert "mis à jour" in (tmp_path / "memory" / "books" / "les-heritiers-d-orion.md").read_text(
        encoding="utf-8"
    )


def test_books_reject_invalid_slug_and_missing_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    client = TestClient(create_app())

    invalid_create = client.post(
        "/books",
        json={
            "title": "Secret",
            "slug": "../secret",
            "content": "# Secret",
        },
    )
    assert invalid_create.status_code == 200
    assert invalid_create.json()["error"]["code"] == "INVALID_BOOK_SLUG"

    invalid_read = client.get("/books/book.md")
    assert invalid_read.status_code == 200
    assert invalid_read.json()["error"]["code"] == "INVALID_BOOK_SLUG"

    missing = client.get("/books/missing-book")
    assert missing.status_code == 200
    assert missing.json()["error"]["code"] == "BOOK_NOT_FOUND"

    invalid_update = client.put(
        "/books/book.md",
        json={
            "title": "Secret",
            "content": "# Secret",
        },
    )
    assert invalid_update.status_code == 200
    assert invalid_update.json()["error"]["code"] == "INVALID_BOOK_SLUG"


def test_review_run_mock_creates_hitl_session(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimé.",
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
    assert [step["name"] for step in body["result"]["hitl"]["steps"]] == ["pitch_options", "review"]


def test_review_run_defaults_to_mock_provider(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/review/run",
        json={
            "book_slug": "alchemised",
            "user_opinion": "J'ai aimé.",
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
            "user_opinion": "J'ai aimé.",
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
            "user_opinion": "J'ai aimé.",
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
    assert "storyboard" not in body["result"]
    assert "prompts" not in body["result"]
    assert "song" in body["result"]
    assert "song_final" in body["result"]
    assert [step["name"] for step in body["result"]["hitl"]["steps"]] == ["song_options", "song"]


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


def test_image_run_requires_book_slug(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/image/run",
        json={
            "lyrics": "Paroles validées",
            "visual_style_id": "lego",
            "provider": "mock",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": True,
        },
    )

    assert response.status_code == 422


def test_image_run_mock_includes_book_slug(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_workspace(tmp_path)
    client = TestClient(create_app())

    response = client.post(
        "/image/run",
        json={
            "book_slug": "alchemised",
            "lyrics": "Paroles validées",
            "visual_style_id": "lego",
            "platform": "instagram",
            "format": "4:5",
            "brief": "Créer des visuels",
            "provider": "mock",
            "model": None,
            "temperature": 0.7,
            "hitl_enabled": False,
            "export_formats": [],
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True, body
    assert body["book_slug"] == "alchemised"
    assert body["result"]["book_slug"] == "alchemised"
    assert body["result"]["book_context"]["book_slug"] == "alchemised"


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
            "step_id": "pitch_options",
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
