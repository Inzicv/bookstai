"""Song workflow orchestrator for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..agents.art_director import ArtDirectorAgent
from ..agents.comedy_room import ComedyRoomAgent
from ..agents.context_builder import ContextBuilder
from ..agents.prompt_maker import PromptMakerAgent
from ..agents.song_writer import SongWriterAgent
from ..agents.style_memory import StyleMemoryAgent
from ..hitl import HITLSession
from ..llm.client import LLMClient


class SongWorkflow:
    """Orchestrate the song generation workflow without image generation."""

    def __init__(
        self,
        memory_root: Path,
        prompt_root: Path,
        llm_client: LLMClient,
        **_: Any,
    ) -> None:
        self.context_builder = ContextBuilder(memory_root=memory_root)
        self.style_memory_agent = StyleMemoryAgent(memory_root=memory_root)
        self.comedy_room_agent = ComedyRoomAgent(prompt_root=prompt_root, llm_client=llm_client)
        self.song_writer_agent = SongWriterAgent(prompt_root=prompt_root, llm_client=llm_client)
        self.art_director_agent = ArtDirectorAgent(prompt_root=prompt_root, llm_client=llm_client)
        self.prompt_maker_agent = PromptMakerAgent(prompt_root=prompt_root, llm_client=llm_client)

    def run(
        self,
        book_slug: str,
        story_scope: str = "pitch_only",
        song_style: str = "parody",
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        return self._run_steps(
            book_slug=book_slug,
            story_scope=story_scope,
            song_style=song_style,
            legacy_kwargs=legacy_kwargs,
        )

    def run_with_hitl(
        self,
        book_slug: str,
        story_scope: str = "pitch_only",
        song_style: str = "parody",
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        result = self._run_steps(
            book_slug=book_slug,
            story_scope=story_scope,
            song_style=song_style,
            legacy_kwargs=legacy_kwargs,
        )
        session = HITLSession(workflow_name="song", item_slug=book_slug)
        session.add_step(name="comedy", content=result["comedy"])
        session.add_step(name="song", content=result["song"])
        session.add_step(name="storyboard", content=result["storyboard"])
        session.add_step(name="prompts", content=result["prompts"])
        session.add_step(name="social", content=result["social"])
        result["hitl"] = session.to_dict()
        return result

    def _run_steps(
        self,
        book_slug: str,
        story_scope: str,
        song_style: str,
        legacy_kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = self.context_builder.build(
            book_slug=book_slug,
            workflow_type="song",
            spoiler_level=story_scope,
        )
        style = self.style_memory_agent.build()
        comedy = self.comedy_room_agent.generate(book_context=context, style_context=style)
        song = self.song_writer_agent.generate(
            book_context=context,
            style_context=style,
            comedy_bank=comedy,
            story_scope=story_scope,
            song_style=song_style,
        )
        storyboard = self.art_director_agent.generate(
            book_context=context,
            style_context=style,
            validated_song=song.get("response", song),
        )
        prompts = self.prompt_maker_agent.generate(validated_storyboard=storyboard)
        return {
            "workflow": "song",
            "book_slug": book_slug,
            "story_scope": story_scope,
            "song_style": song_style,
            "context": context,
            "style": style,
            "song_options": comedy,
            "song": song,
            "storyboard": storyboard,
            "prompts": prompts,
            "song_final": song.get("response", ""),
            "legacy": legacy_kwargs or {},
        }
