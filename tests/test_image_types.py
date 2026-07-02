"""Tests for image generation types."""

from bookstai.image.types import (
    ImageBackendHealthResult,
    ImageGenerationParams,
    ImageGenerationRequest,
    ImageGenerationResult,
)


def test_image_generation_params_to_dict() -> None:
    params = ImageGenerationParams(width=512, height=768, steps=30, cfg=6.5, seed=42, sampler="euler", model="sdxl", workflow_path="wf.json", output_dir="out")

    assert params.to_dict() == {
        "width": 512,
        "height": 768,
        "steps": 30,
        "cfg": 6.5,
        "seed": 42,
        "sampler": "euler",
        "model": "sdxl",
        "workflow_path": "wf.json",
        "output_dir": "out",
    }


def test_image_generation_request_to_dict() -> None:
    request = ImageGenerationRequest(prompt="a paper diorama", negative_prompt="blurry", backend="comfyui")

    data = request.to_dict()
    assert data["prompt"] == "a paper diorama"
    assert data["negative_prompt"] == "blurry"
    assert data["backend"] == "comfyui"
    assert "params" in data


def test_image_generation_result_to_dict() -> None:
    result = ImageGenerationResult(
        ok=True,
        backend="mock",
        image_path="outputs/mock/image.png",
        prompt="a paper diorama",
        negative_prompt="blurry",
        params={"width": 1024},
    )

    assert result.to_dict() == {
        "ok": True,
        "backend": "mock",
        "image_path": "outputs/mock/image.png",
        "prompt": "a paper diorama",
        "negative_prompt": "blurry",
        "params": {"width": 1024},
        "error_code": None,
        "error_message": None,
    }


def test_image_backend_health_result_to_dict() -> None:
    health = ImageBackendHealthResult(ok=True, backend="mock", message="ok")

    assert health.to_dict() == {"ok": True, "backend": "mock", "message": "ok"}
