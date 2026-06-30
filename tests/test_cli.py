"""Tests for the BookstAI CLI."""

from pathlib import Path

from bookstai import cli


class DummySettings:
    def __init__(self, memory_root: Path) -> None:
        self.memory_root = memory_root


def test_main_review_returns_zero(monkeypatch) -> None:
    class DummyWorkflow:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def run(self, **kwargs):
            return {"workflow": "review"}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    exit_code = cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--memory-root",
        "custom/memory",
        "--prompt-root",
        "custom/prompts",
    ])

    assert exit_code == 0


def test_main_song_returns_zero(monkeypatch) -> None:
    class DummyWorkflow:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def run(self, **kwargs):
            return {"workflow": "song"}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", lambda **kwargs: "mock-image-backend")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    exit_code = cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--memory-root",
        "custom/memory",
        "--prompt-root",
        "custom/prompts",
    ])

    assert exit_code == 0


def test_cli_review_calls_workflow(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["memory_root"] = memory_root
            captured["prompt_root"] = prompt_root
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "review"}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main(["review", "--book", "alchemised", "--opinion", "J'ai adoré", "--platform", "instagram"])

    assert captured["llm_client"] == "mock-client"
    assert captured["run"] == {
        "book_slug": "alchemised",
        "user_opinion": "J'ai adoré",
        "platform": "instagram",
    }
    assert "hitl" not in captured


def test_cli_review_hitl_calls_run_with_hitl(monkeypatch) -> None:
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

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--hitl",
    ])

    assert "run" not in captured
    assert captured["run_with_hitl"] == {
        "book_slug": "alchemised",
        "user_opinion": "J'ai adoré",
        "platform": "instagram",
    }


def test_cli_song_calls_workflow(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["memory_root"] = memory_root
            captured["prompt_root"] = prompt_root
            captured["llm_client"] = llm_client
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "song"}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", lambda **kwargs: "mock-image-backend")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
    ])

    assert captured["llm_client"] == "mock-client"
    assert captured["image_backend"] == "mock-image-backend"
    assert captured["run"] == {
        "book_slug": "alchemised",
        "spoiler_mode": "spoiler_free",
        "prompt_type": "scene",
        "platform": "instagram",
    }
    assert "hitl" not in captured


def test_cli_song_hitl_calls_run_with_hitl(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            pass

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "song"}

        def run_with_hitl(self, **kwargs):
            captured["run_with_hitl"] = kwargs
            return {"workflow": "song", "hitl": {"workflow_name": "song"}}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", lambda **kwargs: "mock-image-backend")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--hitl",
    ])

    assert "run" not in captured
    assert captured["run_with_hitl"] == {
        "book_slug": "alchemised",
        "spoiler_mode": "spoiler_free",
        "prompt_type": "scene",
        "platform": "instagram",
    }


def test_cli_accepts_memory_and_prompt_roots(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["memory_root"] = memory_root
            captured["prompt_root"] = prompt_root

        def run(self, **kwargs):
            return {"workflow": "review"}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--memory-root",
        "custom/memory",
        "--prompt-root",
        "custom/prompts",
    ])

    assert captured["memory_root"] == Path("custom/memory")
    assert captured["prompt_root"] == Path("custom/prompts")


def test_cli_review_defaults_to_mock_provider(monkeypatch) -> None:
    captured = {}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["provider"] = provider
        captured["model"] = model
        captured["temperature"] = temperature
        return "mock-client"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            return {"workflow": "review"}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", fake_create_llm_client)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
    ])

    assert captured == {
        "provider": "mock",
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "llm_client": "mock-client",
    }


def test_cli_hitl_does_not_change_review_defaults(monkeypatch) -> None:
    captured = {}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["provider"] = provider
        captured["model"] = model
        captured["temperature"] = temperature
        return "mock-client"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            pass

        def run_with_hitl(self, **kwargs):
            captured["run_with_hitl"] = kwargs
            return {"workflow": "review", "hitl": {"workflow_name": "review"}}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", fake_create_llm_client)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--hitl",
    ])

    assert captured["provider"] == "mock"
    assert captured["model"] == "gpt-4o-mini"
    assert captured["temperature"] == 0.7


def test_cli_review_accepts_openai_provider_configuration(monkeypatch) -> None:
    captured = {}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["provider"] = provider
        captured["model"] = model
        captured["temperature"] = temperature
        return "openai-client"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            return {"workflow": "review"}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", fake_create_llm_client)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--provider",
        "openai",
        "--model",
        "gpt-4o-mini",
        "--temperature",
        "0.3",
    ])

    assert captured == {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "llm_client": "openai-client",
    }


def test_cli_song_defaults_to_mock_image_backend(monkeypatch) -> None:
    captured = {}

    def fake_create_image_backend(**kwargs):
        captured.update(kwargs)
        return "mock-image-backend"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            return {"workflow": "song"}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", fake_create_image_backend)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
    ])

    assert captured["backend"] == "mock"
    assert captured["image_path"] == "outputs/mock/image.png"
    assert captured["image_backend"] == "mock-image-backend"


def test_cli_hitl_does_not_change_song_defaults(monkeypatch) -> None:
    captured = {}

    def fake_create_llm_client(*, provider, model, temperature):
        captured["provider"] = provider
        captured["model"] = model
        captured["temperature"] = temperature
        return "mock-client"

    def fake_create_image_backend(**kwargs):
        captured["image_factory"] = kwargs
        return "mock-image-backend"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            pass

        def run_with_hitl(self, **kwargs):
            captured["run_with_hitl"] = kwargs
            return {"workflow": "song", "hitl": {"workflow_name": "song"}}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", fake_create_llm_client)
    monkeypatch.setattr(cli, "create_image_backend", fake_create_image_backend)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--hitl",
    ])

    assert captured["provider"] == "mock"
    assert captured["model"] == "gpt-4o-mini"
    assert captured["temperature"] == 0.7
    assert captured["image_factory"]["backend"] == "mock"


def test_cli_song_accepts_custom_mock_image_path(monkeypatch) -> None:
    captured = {}

    def fake_create_image_backend(**kwargs):
        captured.update(kwargs)
        return "mock-image-backend"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            return {"workflow": "song"}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", fake_create_image_backend)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--image-backend",
        "mock",
        "--image-path",
        "outputs/mock/custom.png",
    ])

    assert captured["backend"] == "mock"
    assert captured["image_path"] == "outputs/mock/custom.png"


def test_cli_song_accepts_comfyui_image_backend_configuration(monkeypatch) -> None:
    captured = {}

    def fake_create_image_backend(**kwargs):
        captured.update(kwargs)
        return "comfyui-backend"

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            return {"workflow": "song"}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", fake_create_image_backend)
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--image-backend",
        "comfyui",
        "--comfyui-url",
        "http://127.0.0.1:8188",
        "--comfyui-workflow-path",
        "workflows/comfyui/bookstai.json",
        "--image-output-dir",
        "outputs/images",
        "--image-timeout",
        "30",
        "--image-poll-interval",
        "0.5",
    ])

    assert captured["backend"] == "comfyui"
    assert captured["comfyui_url"] == "http://127.0.0.1:8188"
    assert captured["workflow_path"] == "workflows/comfyui/bookstai.json"
    assert captured["output_dir"] == "outputs/images"
    assert captured["timeout"] == 30.0
    assert captured["poll_interval"] == 0.5
    assert captured["image_backend"] == "comfyui-backend"


def test_cli_review_without_export_does_not_call_export_service(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            captured["llm_client"] = llm_client

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "review"}

    class ForbiddenExportService:
        def __init__(self, *args, **kwargs) -> None:
            captured["export_service"] = True

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", ForbiddenExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    exit_code = cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
    ])

    assert exit_code == 0
    assert "export_service" not in captured


def test_cli_song_without_export_does_not_call_export_service(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            captured["image_backend"] = image_backend

        def run(self, **kwargs):
            captured["run"] = kwargs
            return {"workflow": "song"}

    class ForbiddenExportService:
        def __init__(self, *args, **kwargs) -> None:
            captured["export_service"] = True

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", ForbiddenExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", lambda **kwargs: "mock-image-backend")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    exit_code = cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
    ])

    assert exit_code == 0
    assert "export_service" not in captured


def test_cli_review_exports_markdown(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            pass

        def run(self, **kwargs):
            return {"workflow": "review", "book_slug": "alchemised"}

    class DummyExportService:
        def __init__(self, output_root) -> None:
            captured["output_root"] = output_root

        def export(self, workflow_name, item_slug, data, formats):
            captured["export"] = {
                "workflow_name": workflow_name,
                "item_slug": item_slug,
                "data": data,
                "formats": formats,
            }
            return {"markdown": Path("custom_outputs/review.md")}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", DummyExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--export",
        "markdown",
        "--output-root",
        "custom_outputs",
    ])

    assert captured["output_root"] == Path("custom_outputs")
    assert captured["export"] == {
        "workflow_name": "review",
        "item_slug": "alchemised",
        "data": {"workflow": "review", "book_slug": "alchemised"},
        "formats": ["markdown"],
    }


def test_cli_review_exports_json_with_hitl(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            pass

        def run_with_hitl(self, **kwargs):
            return {
                "workflow": "review",
                "book_slug": "alchemised",
                "hitl": {"workflow_name": "review", "item_slug": "alchemised", "steps": []},
            }

    class DummyExportService:
        def __init__(self, output_root) -> None:
            captured["output_root"] = output_root

        def export(self, workflow_name, item_slug, data, formats):
            captured["export"] = {
                "workflow_name": workflow_name,
                "item_slug": item_slug,
                "data": data,
                "formats": formats,
            }
            return {"json": Path("custom_outputs/review.json")}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", DummyExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--hitl",
        "--export",
        "json",
        "--output-root",
        "custom_outputs",
    ])

    assert captured["export"]["workflow_name"] == "review"
    assert "hitl" in captured["export"]["data"]


def test_cli_review_exports_markdown_and_json(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client) -> None:
            pass

        def run(self, **kwargs):
            return {"workflow": "review"}

    class DummyExportService:
        def __init__(self, output_root) -> None:
            captured["output_root"] = output_root

        def export(self, workflow_name, item_slug, data, formats):
            captured["formats"] = formats
            return {}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", DummyExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "review",
        "--book",
        "alchemised",
        "--opinion",
        "J'ai adoré",
        "--platform",
        "instagram",
        "--export",
        "markdown",
        "json",
    ])

    assert captured["output_root"] == Path("outputs")
    assert captured["formats"] == ["markdown", "json"]


def test_cli_song_exports_json(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            pass

        def run(self, **kwargs):
            return {"workflow": "song", "book_slug": "alchemised"}

    class DummyExportService:
        def __init__(self, output_root) -> None:
            captured["output_root"] = output_root

        def export(self, workflow_name, item_slug, data, formats):
            captured["export"] = {
                "workflow_name": workflow_name,
                "item_slug": item_slug,
                "data": data,
                "formats": formats,
            }
            return {"json": Path("custom_outputs/song.json")}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", DummyExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", lambda **kwargs: "mock-image-backend")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--export",
        "json",
        "--output-root",
        "custom_outputs",
    ])

    assert captured["output_root"] == Path("custom_outputs")
    assert captured["export"] == {
        "workflow_name": "song",
        "item_slug": "alchemised",
        "data": {"workflow": "song", "book_slug": "alchemised"},
        "formats": ["json"],
    }


def test_cli_song_exports_json_with_hitl(monkeypatch) -> None:
    captured = {}

    class DummyWorkflow:
        def __init__(self, memory_root, prompt_root, llm_client, image_backend) -> None:
            pass

        def run_with_hitl(self, **kwargs):
            return {
                "workflow": "song",
                "book_slug": "alchemised",
                "hitl": {"workflow_name": "song", "item_slug": "alchemised", "steps": []},
            }

    class DummyExportService:
        def __init__(self, output_root) -> None:
            captured["output_root"] = output_root

        def export(self, workflow_name, item_slug, data, formats):
            captured["export"] = {
                "workflow_name": workflow_name,
                "item_slug": item_slug,
                "data": data,
                "formats": formats,
            }
            return {"json": Path("custom_outputs/song.json")}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "ExportService", DummyExportService)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "create_image_backend", lambda **kwargs: "mock-image-backend")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main([
        "song",
        "--book",
        "alchemised",
        "--spoiler-mode",
        "spoiler_free",
        "--prompt-type",
        "scene",
        "--platform",
        "instagram",
        "--hitl",
        "--export",
        "json",
        "--output-root",
        "custom_outputs",
    ])

    assert captured["export"]["workflow_name"] == "song"
    assert "hitl" in captured["export"]["data"]


def test_cli_rejects_invalid_export_format(monkeypatch) -> None:
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "create_llm_client", lambda **kwargs: "mock-client")
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    try:
        cli.main([
            "review",
            "--book",
            "alchemised",
            "--opinion",
            "J'ai adoré",
            "--platform",
            "instagram",
            "--export",
            "pdf",
        ])
        assert False, "SystemExit expected"
    except SystemExit as exc:
        assert exc.code != 0
