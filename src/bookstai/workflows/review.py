"""Review workflow orchestrator for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..agents.comedy_room import ComedyRoomAgent
from ..agents.context_builder import ContextBuilder
from ..hitl import HITLSession
from ..agents.review_writer import ReviewWriterAgent
from ..agents.style_memory import StyleMemoryAgent
from ..llm.client import LLMClient


class ReviewWorkflow:
    """Orchestrate the review generation workflow."""

    def __init__(
        self,
        memory_root: Path,
        prompt_root: Path,
        llm_client: LLMClient,
    ) -> None:
        self.context_builder = ContextBuilder(memory_root=memory_root)
        self.style_memory_agent = StyleMemoryAgent(memory_root=memory_root)
        self.comedy_room_agent = ComedyRoomAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        self.review_writer_agent = ReviewWriterAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
    def run(
        self,
        book_slug: str,
        user_opinion: str,
    ) -> dict[str, Any]:
        return self._run_steps(
            book_slug=book_slug,
            user_opinion=user_opinion,
        )

    def run_with_hitl(
        self,
        book_slug: str,
        user_opinion: str,
    ) -> dict[str, Any]:
        result = self._run_steps(
            book_slug=book_slug,
            user_opinion=user_opinion,
        )
        session = HITLSession(
            workflow_name="review",
            item_slug=book_slug,
        )
        session.add_step(name="comedy", content=result["comedy"])
        session.add_step(name="review", content=result["review"])
        result["hitl"] = session.to_dict()
        return result

    def _run_steps(
        self,
        book_slug: str,
        user_opinion: str,
    ) -> dict[str, Any]:
        context = self.context_builder.build(
            book_slug=book_slug,
            workflow_type="review",
            spoiler_level="none",
        )
        style = self.style_memory_agent.build()
        comedy = self.comedy_room_agent.generate(
            book_context=context,
            style_context=style,
        )
        review = self.review_writer_agent.generate(
            book_context=context,
            style_context=style,
            comedy_bank=comedy,
            user_opinion=user_opinion,
        )

        return {
            "workflow": "review",
            "book_slug": book_slug,
            "context": context,
            "style": style,
            "comedy": comedy,
            "review": review,
            "pitch_options": comedy,
            "review_final": review["response"],
        }
