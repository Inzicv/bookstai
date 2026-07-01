"""FastAPI application entrypoint for BookstAI."""

from __future__ import annotations

from fastapi import FastAPI

from .routes.health import router as health_router
from .routes.hitl import router as hitl_router
from .routes.learning import router as learning_router
from .routes.review import router as review_router
from .routes.song import router as song_router


def create_app() -> FastAPI:
    app = FastAPI(title="BookstAI", version="8.1")
    app.include_router(health_router)
    app.include_router(review_router)
    app.include_router(song_router)
    app.include_router(hitl_router)
    app.include_router(learning_router)
    return app


app = create_app()

