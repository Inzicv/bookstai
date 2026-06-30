"""Command-line interface for BookstAI."""

from __future__ import annotations

import argparse
from pathlib import Path
from pprint import pprint
from typing import Sequence

from .core.config import load_settings
from .image.mock_backend import MockImageBackend
from .llm.mock import MockLLMClient
from .workflows.review import ReviewWorkflow
from .workflows.song import SongWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bookstai")
    subparsers = parser.add_subparsers(dest="command", required=True)

    review_parser = subparsers.add_parser("review")
    review_parser.add_argument("--book", required=True)
    review_parser.add_argument("--opinion", required=True)
    review_parser.add_argument("--platform", required=True)
    review_parser.add_argument("--memory-root")
    review_parser.add_argument("--prompt-root")

    song_parser = subparsers.add_parser("song")
    song_parser.add_argument("--book", required=True)
    song_parser.add_argument("--spoiler-mode", required=True)
    song_parser.add_argument("--prompt-type", required=True)
    song_parser.add_argument("--platform", required=True)
    song_parser.add_argument("--memory-root")
    song_parser.add_argument("--prompt-root")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    settings = load_settings(
        memory_root=args.memory_root,
        output_root=None,
    )
    memory_root = Path(args.memory_root) if args.memory_root else settings.memory_root
    prompt_root = Path(args.prompt_root) if args.prompt_root else Path("prompts")

    llm_client = MockLLMClient()

    if args.command == "review":
        workflow = ReviewWorkflow(
            memory_root=memory_root,
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        result = workflow.run(
            book_slug=args.book,
            user_opinion=args.opinion,
            platform=args.platform,
        )
    else:
        workflow = SongWorkflow(
            memory_root=memory_root,
            prompt_root=prompt_root,
            llm_client=llm_client,
            image_backend=MockImageBackend(image_path="outputs/mock/image.png"),
        )
        result = workflow.run(
            book_slug=args.book,
            spoiler_mode=args.spoiler_mode,
            prompt_type=args.prompt_type,
            platform=args.platform,
        )

    pprint(result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
