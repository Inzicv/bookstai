"""ComfyUI image backend for BookstAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib import error, request

from ..core.errors import EmptyPromptError, ImageGenerationError
from .backend import ImageBackend


class _StdlibHTTPClient:
    """Small HTTP client wrapper built on the standard library."""

    def post_json(self, url: str, payload: dict[str, object], timeout: float) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except error.URLError as exc:  # pragma: no cover - network failures are not exercised in tests
            raise ImageGenerationError("Failed to contact the ComfyUI backend.") from exc

        if not body.strip():
            return {}
        return json.loads(body)


class ComfyUIImageBackend(ImageBackend):
    def __init__(
        self,
        comfyui_url: str = "http://127.0.0.1:8188",
        workflow_path: str | Path | None = None,
        output_dir: str | Path = "outputs/images",
        timeout: float = 60.0,
        poll_interval: float = 1.0,
        http_client: Any | None = None,
    ) -> None:
        self.comfyui_url = comfyui_url
        self.workflow_path = Path(workflow_path) if workflow_path is not None else None
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.http_client = http_client or _StdlibHTTPClient()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise EmptyPromptError("Prompt must not be empty.")

        payload: dict[str, object] = {"prompt": prompt}
        if self.workflow_path is not None:
            payload["workflow_path"] = str(self.workflow_path)

        response = self.http_client.post_json(
            self.comfyui_url,
            payload,
            timeout=self.timeout,
        )

        image_path = response.get("image_path")
        if isinstance(image_path, str) and image_path.strip():
            return image_path

        raise ImageGenerationError("ComfyUI response did not contain an image path.")
