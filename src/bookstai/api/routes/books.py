"""Book library routes."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from ..schemas.books import BookCreateRequest, BookUpdateRequest
from .shared import api_error, build_memory_root, serialize_path

router = APIRouter(prefix="/books", tags=["books"])

BOOK_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _books_dir() -> Path:
    return build_memory_root() / "books"


def _book_path(slug: str) -> Path:
    return _books_dir() / f"{slug}.md"


def _validate_slug(slug: str) -> bool:
    return bool(BOOK_SLUG_PATTERN.fullmatch(slug))


def _extract_title(content: str, fallback_slug: str) -> str:
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip() or fallback_slug
    return fallback_slug


@router.get("")
def list_books() -> dict[str, Any]:
    books_dir = _books_dir()
    books: list[dict[str, str]] = []
    if books_dir.exists():
        for path in sorted(books_dir.glob("*.md")):
            slug = path.stem
            content = path.read_text(encoding="utf-8")
            books.append(
                {
                    "slug": slug,
                    "title": _extract_title(content, slug),
                    "path": serialize_path(path) or path.as_posix(),
                }
            )
    return {"ok": True, "books": books}


@router.get("/{slug}")
def read_book(slug: str) -> dict[str, Any]:
    if not _validate_slug(slug):
        return api_error(
            "INVALID_BOOK_SLUG",
            "Book slug must contain only lowercase letters, numbers and hyphens.",
        )

    path = _book_path(slug)
    if not path.exists():
        return api_error("BOOK_NOT_FOUND", "Book file not found.")

    content = path.read_text(encoding="utf-8")
    return {
        "ok": True,
        "book": {
            "slug": slug,
            "title": _extract_title(content, slug),
            "content": content,
        },
    }


@router.post("")
def create_book(payload: BookCreateRequest) -> dict[str, Any]:
    if not _validate_slug(payload.slug):
        return api_error(
            "INVALID_BOOK_SLUG",
            "Book slug must contain only lowercase letters, numbers and hyphens.",
        )

    books_dir = _books_dir()
    books_dir.mkdir(parents=True, exist_ok=True)
    path = _book_path(payload.slug)
    if path.exists():
        return api_error("BOOK_ALREADY_EXISTS", "A book with this slug already exists.")

    path.write_text(payload.content, encoding="utf-8")
    return {
        "ok": True,
        "book": {
            "slug": payload.slug,
            "title": payload.title,
            "path": serialize_path(path) or path.as_posix(),
        },
    }


@router.put("/{slug}")
def update_book(slug: str, payload: BookUpdateRequest) -> dict[str, Any]:
    if not _validate_slug(slug):
        return api_error(
            "INVALID_BOOK_SLUG",
            "Book slug must contain only lowercase letters, numbers and hyphens.",
        )

    path = _book_path(slug)
    if not path.exists():
        return api_error("BOOK_NOT_FOUND", "Book file not found.")

    path.write_text(payload.content, encoding="utf-8")
    return {
        "ok": True,
        "book": {
            "slug": slug,
            "title": payload.title,
            "path": serialize_path(path) or path.as_posix(),
        },
    }
