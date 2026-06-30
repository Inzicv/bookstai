"""Tests for the external Langflow Song custom component file."""

from pathlib import Path


def test_langflow_song_custom_component_file_has_expected_contract() -> None:
    component_file = Path("langflow_components/bookstai/bookstai_song_component.py")

    assert component_file.exists()

    content = component_file.read_text(encoding="utf-8")

    assert "BookstAISongComponent" in content
    assert "from bookstai.langflow.song_component import run_song_workflow" in content
    assert "book_slug" in content
    assert "spoiler_mode" in content
    assert "prompt_type" in content
    assert "platform" in content
    assert "provider" in content
    assert "model" in content
    assert "temperature" in content
    assert "memory_root" in content
    assert "prompt_root" in content
    assert "image_path" in content
    assert "image_backend" in content
    assert "comfyui_url" in content
    assert "comfyui_workflow_path" in content
    assert "image_output_dir" in content
    assert "image_timeout" in content
    assert "image_poll_interval" in content
    assert "hitl" in content
    assert "provider=self.provider" in content
    assert "model=self.model" in content
    assert "temperature=float(self.temperature)" in content
    assert "image_backend=self.image_backend" in content
    assert "comfyui_url=self.comfyui_url" in content
    assert "image_timeout=float(self.image_timeout)" in content
    assert "image_poll_interval=float(self.image_poll_interval)" in content
    assert "hitl=_to_bool(self.hitl)" in content
    assert "openai" not in content.lower()
    assert "requests." not in content.lower()
    assert "httpx." not in content.lower()
    assert "urllib" not in content.lower()
    assert "OPENAI_API_KEY" not in content
    assert "return Data(value=result)" in content
