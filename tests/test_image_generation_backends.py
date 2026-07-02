from __future__ import annotations

from pathlib import Path

import pytest

from bookstai.core.errors import ImageGenerationError, MissingAPIKeyError
from bookstai.image_generation.mock_backend import MockImageBackend
from bookstai.image_generation.openai_backend import OpenAIImageBackend
from bookstai.image_generation.types import ImageGenerationRequest


def _request(tmp_path: Path) -> ImageGenerationRequest:
    return ImageGenerationRequest(
        item_slug="mockingbird-lego-test",
        storyboard={"scenes": [{"scene_id": "scene_001"}]},
        character_prompts=[{"prompt_id": "character_001", "status": "approved"}],
        background_prompts=[{"prompt_id": "background_001", "status": "approved"}],
        confirm_generation=True,
    )


def test_mock_backend_writes_generation_json(tmp_path: Path) -> None:
    backend = MockImageBackend(output_root=tmp_path / "outputs")
    result = backend.generate_batch(_request(tmp_path))

    assert result.ok is True
    assert (tmp_path / "outputs" / "mockingbird-lego-test" / "generation.json").exists()
    assert result.images[0].scene_id == "scene_001"


def test_openai_backend_requires_api_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    backend = OpenAIImageBackend(output_root=tmp_path / "outputs", model="gpt-image-2")

    with pytest.raises(MissingAPIKeyError):
        backend.generate_batch(_request(tmp_path))

