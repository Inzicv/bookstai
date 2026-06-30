"""ComfyUI image backend for BookstAI."""

from __future__ import annotations

import copy
import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib import error, request

from ..core.errors import (
    EmptyPromptError,
    ImageBackendConnectionError,
    ImageGenerationError,
)
from .backend import ImageBackend

BOOKSTAI_PROMPT_PLACEHOLDER = "__BOOKSTAI_PROMPT__"


class ComfyUIHTTPClient:
    """Small HTTP client wrapper built on the standard library."""

    def post_json(self, url: str, payload: dict[str, object], timeout: float) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return self._request_json(req, timeout)

    def get_json(self, url: str, timeout: float) -> dict[str, Any]:
        req = request.Request(url, method="GET")
        return self._request_json(req, timeout)

    def get_bytes(self, url: str, timeout: float) -> bytes:
        req = request.Request(url, method="GET")
        try:
            with request.urlopen(req, timeout=timeout) as response:
                body = response.read()
        except (error.URLError, TimeoutError, ValueError, OSError) as exc:
            raise ImageBackendConnectionError("Could not reach ComfyUI backend.") from exc

        if not body:
            raise ImageBackendConnectionError("Could not reach ComfyUI backend.")

        return body

    def _request_json(self, req: request.Request, timeout: float) -> dict[str, Any]:
        try:
            with request.urlopen(req, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except (error.URLError, TimeoutError, ValueError, OSError) as exc:
            raise ImageBackendConnectionError("Could not reach ComfyUI backend.") from exc

        if not body.strip():
            raise ImageBackendConnectionError("Could not reach ComfyUI backend.")

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ImageBackendConnectionError("Could not reach ComfyUI backend.") from exc

        if not isinstance(parsed, dict):
            raise ImageBackendConnectionError("Could not reach ComfyUI backend.")

        return parsed


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
        self.http_client = http_client or ComfyUIHTTPClient()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise EmptyPromptError("Prompt must not be empty.")

        if self.workflow_path is None:
            return self._generate_compatibility_path(prompt)

        workflow = self._load_workflow()
        workflow_with_prompt = self._inject_prompt(workflow, prompt)
        response = self.http_client.post_json(
            f"{self.comfyui_url}/prompt",
            {"prompt": workflow_with_prompt},
            timeout=self.timeout,
        )

        prompt_id = response.get("prompt_id")
        if not isinstance(prompt_id, str) or not prompt_id.strip():
            image_path = response.get("image_path")
            if isinstance(image_path, str) and image_path.strip():
                return image_path
            raise ImageGenerationError("ComfyUI response did not contain a prompt id.")

        deadline = time.monotonic() + self.timeout
        while time.monotonic() <= deadline:
            history = self.http_client.get_json(
                f"{self.comfyui_url}/history/{prompt_id}",
                timeout=self.timeout,
            )
            image_reference = self._extract_image_reference_from_history(history, prompt_id)
            if image_reference:
                return self._download_image(image_reference)
            if time.monotonic() > deadline:
                break
            time.sleep(self.poll_interval)

        raise ImageGenerationError("ComfyUI image generation timed out.")

    def _generate_compatibility_path(self, prompt: str) -> str:
        response = self.http_client.post_json(
            f"{self.comfyui_url}/prompt",
            {"prompt": prompt},
            timeout=self.timeout,
        )

        image_path = response.get("image_path")
        if isinstance(image_path, str) and image_path.strip():
            return image_path

        raise ImageGenerationError("ComfyUI response did not contain an image path.")

    def _load_workflow(self) -> dict[str, Any]:
        if self.workflow_path is None:
            raise ImageGenerationError("ComfyUI workflow file not found.")

        if not self.workflow_path.exists():
            raise ImageGenerationError("ComfyUI workflow file not found.")

        try:
            raw_workflow = self.workflow_path.read_text(encoding="utf-8")
            parsed = json.loads(raw_workflow)
        except json.JSONDecodeError as exc:
            raise ImageGenerationError("ComfyUI workflow file is invalid JSON.") from exc

        if not isinstance(parsed, dict):
            raise ImageGenerationError("ComfyUI workflow must be a JSON object.")

        return parsed

    def _inject_prompt(self, workflow: dict[str, Any], prompt: str) -> dict[str, Any]:
        workflow_copy = copy.deepcopy(workflow)
        if self._replace_placeholder(workflow_copy, prompt):
            return workflow_copy
        if self._replace_first_clip_text_encode(workflow_copy, prompt):
            return workflow_copy
        raise ImageGenerationError("ComfyUI workflow does not contain a prompt placeholder.")

    def _replace_placeholder(self, value: Any, prompt: str) -> bool:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "text" and item == BOOKSTAI_PROMPT_PLACEHOLDER:
                    value[key] = prompt
                    return True
                if self._replace_placeholder(item, prompt):
                    return True
        elif isinstance(value, list):
            for item in value:
                if self._replace_placeholder(item, prompt):
                    return True
        return False

    def _replace_first_clip_text_encode(self, workflow: dict[str, Any], prompt: str) -> bool:
        for node in workflow.values():
            if not isinstance(node, dict):
                continue
            if node.get("class_type") != "CLIPTextEncode":
                continue
            inputs = node.get("inputs")
            if isinstance(inputs, dict) and "text" in inputs:
                inputs["text"] = prompt
                return True
        return False

    def _download_image(self, image_reference: dict[str, str]) -> str:
        filename = image_reference["filename"]
        subfolder = image_reference["subfolder"]
        image_type = image_reference["type"]
        query = urlencode(
            {
                "filename": filename,
                "subfolder": subfolder,
                "type": image_type,
            }
        )
        url = f"{self.comfyui_url}/view?{query}"
        image_bytes = self.http_client.get_bytes(url, timeout=self.timeout)

        target_path = self._resolve_output_path(filename, subfolder)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(image_bytes)
        return str(target_path)

    def _resolve_output_path(self, filename: str, subfolder: str) -> Path:
        if self._is_dangerous_path_component(filename):
            raise ImageGenerationError("ComfyUI history contained an invalid image reference.")

        safe_filename = Path(filename).name
        if not safe_filename or safe_filename in {".", ".."}:
            raise ImageGenerationError("ComfyUI history contained an invalid image reference.")

        if self._is_dangerous_path_component(subfolder):
            raise ImageGenerationError("ComfyUI history contained an invalid image reference.")

        safe_subfolder = Path(subfolder) if subfolder else Path()
        if any(part == ".." for part in safe_subfolder.parts):
            raise ImageGenerationError("ComfyUI history contained an invalid image reference.")

        relative_target = safe_subfolder / safe_filename
        target_path = self.output_dir / relative_target
        resolved_root = self.output_dir.resolve()
        resolved_target = target_path.resolve()
        if resolved_root not in resolved_target.parents and resolved_target != resolved_root / safe_filename:
            raise ImageGenerationError("ComfyUI history contained an invalid image reference.")
        return target_path

    def _is_dangerous_path_component(self, value: str) -> bool:
        if not value or value in {".", ".."}:
            return True
        if Path(value).is_absolute():
            return True
        if "/" in value or "\\" in value:
            return True
        return ".." in Path(value).parts

    def _extract_image_reference_from_history(self, history: dict[str, Any], prompt_id: str) -> dict[str, str] | None:
        prompt_history = history.get(prompt_id)
        if not isinstance(prompt_history, dict):
            return None

        outputs = prompt_history.get("outputs")
        if not isinstance(outputs, dict):
            return None

        for output in outputs.values():
            if not isinstance(output, dict):
                continue
            images = output.get("images")
            if not isinstance(images, list):
                continue
            for image in images:
                if not isinstance(image, dict):
                    continue
                filename = image.get("filename")
                if not isinstance(filename, str) or not filename.strip():
                    continue
                subfolder = image.get("subfolder")
                image_type = image.get("type")
                return {
                    "filename": filename,
                    "subfolder": subfolder if isinstance(subfolder, str) else "",
                    "type": image_type if isinstance(image_type, str) and image_type.strip() else "output",
                }
        return None
