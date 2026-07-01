"""Book library API schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class BookListItem(BaseModel):
    slug: str
    title: str
    path: str


class BookRecord(BaseModel):
    slug: str
    title: str
    content: str


class BookCreateRequest(BaseModel):
    title: str
    slug: str
    content: str


class BookUpdateRequest(BaseModel):
    title: str
    content: str


class BookListResponse(BaseModel):
    ok: Literal[True]
    books: list[BookListItem]


class BookReadResponse(BaseModel):
    ok: Literal[True]
    book: BookRecord


class BookWriteResponse(BaseModel):
    ok: Literal[True]
    book: BookListItem
