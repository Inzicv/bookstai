"""Tests for the BookstAI CLI."""

from pathlib import Path

from bookstai import cli


class DummySettings:
    def __init__(self, memory_root: Path) -> None:
        self.memory_root = memory_root


def test_main_review_returns_zero(monkeypatch) -> None:
    class DummyWorkflow:
        def __init__(self, *args, **kwargs) -> None:
            self.args = args
            self.kwargs = kwargs

        def run(self, **kwargs):
            self.run_kwargs = kwargs
            return {"workflow": "review"}

    monkeypatch.setattr(cli, "ReviewWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    exit_code = cli.main(
        [
            "review",
            "--book",
            "alchemised",
            "--opinion",
            "J’ai adoré",
            "--platform",
            "instagram",
            "--memory-root",
            "custom/memory",
            "--prompt-root",
            "custom/prompts",
        ]
    )

    assert exit_code == 0


def test_main_song_returns_zero(monkeypatch) -> None:
    class DummyWorkflow:
        def __init__(self, *args, **kwargs) -> None:
            self.args = args
            self.kwargs = kwargs

        def run(self, **kwargs):
            self.run_kwargs = kwargs
            return {"workflow": "song"}

    monkeypatch.setattr(cli, "SongWorkflow", DummyWorkflow)
    monkeypatch.setattr(cli, "load_settings", lambda **kwargs: DummySettings(Path("default/memory")))
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    exit_code = cli.main(
        [
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
        ]
    )

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
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main(["review", "--book", "alchemised", "--opinion", "J’ai adoré", "--platform", "instagram"])

    assert captured["run"] == {
        "book_slug": "alchemised",
        "user_opinion": "J’ai adoré",
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
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main(
        [
            "song",
            "--book",
            "alchemised",
            "--spoiler-mode",
            "spoiler_free",
            "--prompt-type",
            "scene",
            "--platform",
            "instagram",
        ]
    )

    assert captured["run"] == {
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
    monkeypatch.setattr(cli, "pprint", lambda *args, **kwargs: None)

    cli.main(
        [
            "review",
            "--book",
            "alchemised",
            "--opinion",
            "J’ai adoré",
            "--platform",
            "instagram",
            "--memory-root",
            "custom/memory",
            "--prompt-root",
            "custom/prompts",
        ]
    )

    assert str(captured["memory_root"]) == "custom/memory"
    assert str(captured["prompt_root"]) == "custom/prompts"
