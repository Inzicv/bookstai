"""FastAPI application entrypoint for BookstAI."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.health import router as health_router
from .routes.books import router as books_router
from .routes.hitl import router as hitl_router
from .routes.learning import router as learning_router
from .routes.review import router as review_router
from .routes.song import router as song_router


def create_app() -> FastAPI:
    app = FastAPI(title="BookstAI", version="8.1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(books_router)
    app.include_router(review_router)
    app.include_router(song_router)
    app.include_router(hitl_router)
    app.include_router(learning_router)
    return app


app = create_app()
