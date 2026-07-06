"""Pitch workflow orchestrator for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..agents.comedy_room import ComedyRoomAgent
from ..agents.style_memory import StyleMemoryAgent
from ..hitl import HITLSession
from ..llm.client import LLMClient


class PitchWorkflow:
    """Orchestrate the pitch generation workflow."""

    def __init__(
        self,
        memory_root: Path,
        prompt_root: Path,
        llm_client: LLMClient,
    ) -> None:
        self.style_memory_agent = StyleMemoryAgent(memory_root=memory_root)
        self.comedy_room_agent = ComedyRoomAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )

    def run(
        self,
        item_slug: str,
        summary: str,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        style = self.style_memory_agent.build()
        book_context = {
            "source": "user_summary",
            "sections": {
                "résumé fourni": summary,
            },
        }
        pitch_options = self.comedy_room_agent.generate(
            book_context=book_context,
            style_context=style,
        )
        return {
            "workflow": "pitch",
            "item_slug": item_slug,
            "summary": summary,
            "style": style,
            "pitch_options": pitch_options,
            "legacy": legacy_kwargs or {},
        }

    def run_with_hitl(
        self,
        item_slug: str,
        summary: str,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        result = self.run(item_slug=item_slug, summary=summary, **legacy_kwargs)
        session = HITLSession(
            workflow_name="pitch",
            item_slug=item_slug,
        )
        session.add_step(name="pitch_options", content=result["pitch_options"])
        result["hitl"] = session.to_dict()
        return result
