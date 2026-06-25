"""Langflow-friendly nodes for the Review Assistant.

These functions are intentionally small, deterministic, and free of interactive
input so they can be wired into Langflow later as independent nodes.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from src.services.review_assistant_service import ReviewAssistantService


DEFAULT_BOOKS_DIR = "memory/books"
DEFAULT_REVIEWS_PATH = "memory/reviews/reviews.md"
DEFAULT_HUMOR_PATH = "memory/humor/references.md"


def _service_for_slug(slug: str) -> ReviewAssistantService:
    book_path = Path(DEFAULT_BOOKS_DIR) / f"{slug}.md"
    return ReviewAssistantService(
        book_path=str(book_path),
        reviews_path=DEFAULT_REVIEWS_PATH,
        humor_path=DEFAULT_HUMOR_PATH,
    )


def load_review_context(slug: str) -> dict[str, object]:
    """Load the active review context for a single book slug.

    Args:
        slug: File slug in `memory/books/<slug>.md`.

    Returns:
        A plain dictionary containing the review assets needed by later nodes.
    """
    service = _service_for_slug(slug)
    assets = service.load_assets()
    return {
        "slug": slug,
        "book_title": assets.book_title,
        "book_fields": assets.book_fields,
        "previous_pitch": assets.previous_pitch,
        "previous_avis": assets.previous_avis,
        "humor_refs": assets.humor_refs,
        "pitch_anchor": assets.pitch_anchor,
        "avis_anchor": assets.avis_anchor,
    }


def generate_pitch(slug: str) -> dict[str, object]:
    """Generate the pitch proposal for a single book slug.

    Returns:
        A dictionary with the proposal text and supporting ideas.
    """
    service = _service_for_slug(slug)
    assets = service.load_assets()
    step = service.propose_pitch_step(assets)
    return {
        "step_name": step.step_name,
        "title": step.title,
        "content": step.content,
        "options": step.options,
        "notes": step.notes,
    }


def generate_avis(raw_avis: str, validated_pitch: str, slug: str) -> dict[str, object]:
    """Generate the avis proposal from raw user notes and a validated pitch.

    Args:
        raw_avis: User notes captured as raw avis text.
        validated_pitch: The pitch validated by the human.
        slug: File slug in `memory/books/<slug>.md`.

    Returns:
        A dictionary containing the avis proposal and the supplied inputs.
    """
    service = _service_for_slug(slug)
    assets = service.load_assets()
    step = service.propose_avis_step(assets, raw_avis)
    return {
        "step_name": step.step_name,
        "title": step.title,
        "content": step.content,
        "options": step.options,
        "notes": step.notes,
        "validated_pitch": validated_pitch,
        "raw_avis": raw_avis,
    }


def generate_hooks(validated_pitch: str, validated_avis: str, slug: str) -> dict[str, object]:
    """Generate hook proposals from validated pitch and avis.

    Args:
        validated_pitch: The human-validated pitch text.
        validated_avis: The human-validated avis text.
        slug: File slug in `memory/books/<slug>.md`.

    Returns:
        A dictionary with hook suggestions and the validated inputs.
    """
    service = _service_for_slug(slug)
    assets = service.load_assets()
    step = service.propose_hooks_step(assets)
    return {
        "step_name": step.step_name,
        "title": step.title,
        "content": step.content,
        "options": step.options,
        "notes": step.notes,
        "validated_pitch": validated_pitch,
        "validated_avis": validated_avis,
    }


def assemble_review_script(hook: str, pitch: str, avis: str, slug: str) -> dict[str, object]:
    """Assemble the final review script from validated parts.

    Args:
        hook: Human-selected hook.
        pitch: Human-validated pitch.
        avis: Human-validated avis.
        slug: File slug in `memory/books/<slug>.md`.

    Returns:
        A dictionary containing the final script and its metadata.
    """
    service = _service_for_slug(slug)
    assets = service.load_assets()
    step = service.assemble_script_step(
        assets=assets,
        pitch_final=pitch,
        avis_final=avis,
        hook_final=hook,
        user_notes=avis,
    )
    payload = asdict(step)
    payload["slug"] = slug
    return payload
