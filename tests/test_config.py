"""Tests for BookstAI configuration loading."""

from pathlib import Path

from bookstai.core.config import load_settings


def test_load_settings_uses_defaults(monkeypatch) -> None:
    monkeypatch.delenv("BOOKSTAI_MEMORY_ROOT", raising=False)
    monkeypatch.delenv("BOOKSTAI_OUTPUT_ROOT", raising=False)
    monkeypatch.delenv("BOOKSTAI_PROVIDER", raising=False)
    monkeypatch.delenv("BOOKSTAI_MODEL", raising=False)
    monkeypatch.delenv("BOOKSTAI_TEMPERATURE", raising=False)

    settings = load_settings()

    assert settings.memory_root == Path("./memory")
    assert settings.output_root == Path("./output")
    assert settings.provider == "mock"
    assert settings.model == "gpt-4"
    assert settings.temperature == 0.7


def test_load_settings_reads_memory_root(monkeypatch) -> None:
    monkeypatch.setenv("BOOKSTAI_MEMORY_ROOT", "custom/memory")

    settings = load_settings()

    assert settings.memory_root == Path("custom/memory")


def test_load_settings_reads_output_root(monkeypatch) -> None:
    monkeypatch.setenv("BOOKSTAI_OUTPUT_ROOT", "custom/outputs")

    settings = load_settings()

    assert settings.output_root == Path("custom/outputs")


def test_load_settings_reads_provider(monkeypatch) -> None:
    monkeypatch.setenv("BOOKSTAI_PROVIDER", "openai")

    settings = load_settings()

    assert settings.provider == "openai"


def test_load_settings_reads_model(monkeypatch) -> None:
    monkeypatch.setenv("BOOKSTAI_MODEL", "gpt-4.1")

    settings = load_settings()

    assert settings.model == "gpt-4.1"


def test_load_settings_reads_temperature(monkeypatch) -> None:
    monkeypatch.setenv("BOOKSTAI_TEMPERATURE", "1.2")

    settings = load_settings()

    assert settings.temperature == 1.2


def test_load_settings_converts_temperature_to_float(monkeypatch) -> None:
    monkeypatch.setenv("BOOKSTAI_TEMPERATURE", "0.25")

    settings = load_settings()

    assert isinstance(settings.temperature, float)
    assert settings.temperature == 0.25
