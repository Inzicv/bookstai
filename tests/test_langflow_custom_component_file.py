"""Tests for the external Langflow custom component file."""

from pathlib import Path


def test_langflow_custom_component_file_has_expected_contract() -> None:
    component_file = Path("langflow_components/bookstai_review_component.py")

    content = component_file.read_text(encoding="utf-8")

    assert component_file.exists()
    assert "BookstAIReviewComponent" in content
    assert "from bookstai.langflow.review_component import run_review_workflow" in content
    assert "openai" not in content.lower()
    assert "requests." not in content.lower()
    assert "httpx." not in content.lower()
    assert "urllib" not in content.lower()
