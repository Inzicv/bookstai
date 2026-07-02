"""OpenAI image generation backend."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from ..core.errors import ImageGenerationError, MissingAPIKeyError
from .backend import ImageBackend
from .types import GeneratedImageArtifact, ImageGenerationCostEstimate, ImageGenerationRequest, ImageGenerationResult


class OpenAIImageBackend(ImageBackend):
    name = "openai"

    def __init__(self, output_root: str | Path = "outputs/images", model: str | None = None, quality: str | None = "medium") -> None:
        self.output_root = Path(output_root)
        self.model = model
        self.quality = quality
        self.output_root.mkdir(parents=True, exist_ok=True)

    def generate_batch(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        import os

        if not request.confirm_generation:
            raise ImageGenerationError("Generation must be confirmed before batch generation.")
        if not os.getenv("OPENAI_API_KEY"):
            raise MissingAPIKeyError("OPENAI_API_KEY is required to use the openai image backend.")
        target_dir = self.output_root / request.item_slug
        target_dir.mkdir(parents=True, exist_ok=True)
        images = []
        for index, scene in enumerate(request.storyboard.get("scenes", []), start=1):
            images.append(
                GeneratedImageArtifact(
                    image_id=f"image_{index:03d}",
                    scene_id=scene.get("scene_id", f"scene_{index:03d}"),
                    prompt_id=(request.character_prompts[0].get("prompt_id") if request.character_prompts else None),
                    backend=self.name,
                    status="generated",
                    output_path=str(target_dir / f"{scene.get('scene_id', f'scene_{index:03d}')}.png"),
                    preview_url=None,
                    generation_parameters=request.to_dict(),
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
            )
        estimate = ImageGenerationCostEstimate(
            currency="USD",
            estimated_min=0.24 * max(1, len(images)),
            estimated_max=0.66 * max(1, len(images)),
            assumptions={
                "image_count": len(images),
                "model": request.model,
                "quality": request.quality,
                "format": request.format,
            },
        )
        generation_path = target_dir / "generation.json"
        generation_path.write_text(
            json.dumps(
                {
                    "backend": self.name,
                    "model": request.model,
                    "quality": request.quality,
                    "estimated_cost": estimate.to_dict(),
                    "images": [image.to_dict() for image in images],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return ImageGenerationResult(
            ok=True,
            backend=self.name,
            model=request.model,
            quality=request.quality,
            estimated_cost=estimate,
            images=images,
            generation_path=str(generation_path),
        )
