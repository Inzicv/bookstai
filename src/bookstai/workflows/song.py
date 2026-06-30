"""Song workflow orchestrator for BookstAI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..agents.art_director import ArtDirectorAgent
from ..agents.comedy_room import ComedyRoomAgent
from ..agents.context_builder import ContextBuilder
from ..agents.image_gen import ImageGenAgent
from ..agents.prompt_maker import PromptMakerAgent
from ..agents.social_media import SocialMediaAgent
from ..agents.song_writer import SongWriterAgent
from ..agents.style_memory import StyleMemoryAgent
from ..image.backend import ImageBackend
from ..llm.client import LLMClient


class SongWorkflow:
    """Orchestrate the song generation workflow."""

    def __init__(
        self,
        memory_root: Path,
        prompt_root: Path,
        llm_client: LLMClient,
        image_backend: ImageBackend,
    ) -> None:
        self.context_builder = ContextBuilder(memory_root=memory_root)
        self.style_memory_agent = StyleMemoryAgent(memory_root=memory_root)
        self.comedy_room_agent = ComedyRoomAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        self.song_writer_agent = SongWriterAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        self.art_director_agent = ArtDirectorAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        self.prompt_maker_agent = PromptMakerAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        self.image_gen_agent = ImageGenAgent(backend=image_backend)
        self.social_media_agent = SocialMediaAgent(
            prompt_root=prompt_root,
            llm_client=llm_client,
        )

    def run(
        self,
        book_slug: str,
        spoiler_mode: str,
        prompt_type: str,
        platform: str,
    ) -> dict[str, Any]:
        context = self.context_builder.build(
            book_slug=book_slug,
            workflow_type="song",
            spoiler_level="none",
        )
        style = self.style_memory_agent.build()
        comedy = self.comedy_room_agent.generate(
            book_context=context,
            style_context=style,
        )
        song = self.song_writer_agent.generate(
            book_context=context,
            style_context=style,
            comedy_bank=comedy,
            spoiler_mode=spoiler_mode,
        )
        art_direction = self.art_director_agent.generate(
            book_context=context,
            style_context=style,
            validated_content=song["response"],
        )
        image_prompt = self.prompt_maker_agent.generate(
            art_direction=art_direction["response"],
            prompt_type=prompt_type,
        )
        image = self.image_gen_agent.generate(prompt=image_prompt["response"])
        social = self.social_media_agent.generate(
            validated_content=song["response"],
            style_context=style,
            platform=platform,
        )

        return {
            "workflow": "song",
            "book_slug": book_slug,
            "context": context,
            "style": style,
            "comedy": comedy,
            "song": song,
            "art_direction": art_direction,
            "image_prompt": image_prompt,
            "image": image,
            "social": social,
        }
