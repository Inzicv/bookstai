"""Command-line interface for BookstAI."""

from __future__ import annotations

import argparse
from pathlib import Path
from pprint import pprint
from typing import Sequence

from .core.config import load_settings
from .image import create_image_backend
from .exports import ExportService
from .hitl import HITLSessionStorage
from .llm import create_llm_client
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
    review_parser.add_argument("--provider", default="mock")
    review_parser.add_argument("--model", default="gpt-4o-mini")
    review_parser.add_argument("--temperature", type=float, default=0.7)
    review_parser.add_argument("--hitl", action="store_true")
    review_parser.add_argument("--export", nargs="+", choices=["markdown", "json"])
    review_parser.add_argument("--output-root", default="outputs")

    song_parser = subparsers.add_parser("song")
    song_parser.add_argument("--book", required=True)
    song_parser.add_argument("--spoiler-mode", required=True)
    song_parser.add_argument("--prompt-type", required=True)
    song_parser.add_argument("--platform", required=True)
    song_parser.add_argument("--memory-root")
    song_parser.add_argument("--prompt-root")
    song_parser.add_argument("--provider", default="mock")
    song_parser.add_argument("--model", default="gpt-4o-mini")
    song_parser.add_argument("--temperature", type=float, default=0.7)
    song_parser.add_argument("--image-backend", default="mock")
    song_parser.add_argument("--image-path", default="outputs/mock/image.png")
    song_parser.add_argument("--comfyui-url", default="http://127.0.0.1:8188")
    song_parser.add_argument("--comfyui-workflow-path")
    song_parser.add_argument("--image-output-dir", default="outputs/images")
    song_parser.add_argument("--image-timeout", type=float, default=60.0)
    song_parser.add_argument("--image-poll-interval", type=float, default=1.0)
    song_parser.add_argument("--hitl", action="store_true")
    song_parser.add_argument("--export", nargs="+", choices=["markdown", "json"])
    song_parser.add_argument("--output-root", default="outputs")

    hitl_parser = subparsers.add_parser("hitl")
    hitl_subparsers = hitl_parser.add_subparsers(dest="hitl_command", required=True)

    show_parser = hitl_subparsers.add_parser("show")
    show_parser.add_argument("--file", required=True)

    approve_parser = hitl_subparsers.add_parser("approve")
    approve_parser.add_argument("--file", required=True)
    approve_parser.add_argument("--step", required=True)
    approve_parser.add_argument("--comment")

    reject_parser = hitl_subparsers.add_parser("reject")
    reject_parser.add_argument("--file", required=True)
    reject_parser.add_argument("--step", required=True)
    reject_parser.add_argument("--comment")

    edit_parser = hitl_subparsers.add_parser("edit")
    edit_parser.add_argument("--file", required=True)
    edit_parser.add_argument("--step", required=True)
    edit_parser.add_argument("--content", required=True)
    edit_parser.add_argument("--comment")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "hitl":
        return _run_hitl_command(args)

    settings = load_settings(
        memory_root=args.memory_root,
        output_root=None,
    )
    memory_root = Path(args.memory_root) if args.memory_root else settings.memory_root
    prompt_root = Path(args.prompt_root) if args.prompt_root else Path("prompts")

    llm_client = create_llm_client(
        provider=args.provider,
        model=args.model,
        temperature=args.temperature,
    )

    if args.command == "review":
        workflow = ReviewWorkflow(
            memory_root=memory_root,
            prompt_root=prompt_root,
            llm_client=llm_client,
        )
        if args.hitl:
            result = workflow.run_with_hitl(
                book_slug=args.book,
                user_opinion=args.opinion,
                platform=args.platform,
            )
        else:
            result = workflow.run(
                book_slug=args.book,
                user_opinion=args.opinion,
                platform=args.platform,
            )
    else:
        image_backend = create_image_backend(
            backend=args.image_backend,
            image_path=args.image_path,
            comfyui_url=args.comfyui_url,
            workflow_path=args.comfyui_workflow_path,
            output_dir=args.image_output_dir,
            timeout=args.image_timeout,
            poll_interval=args.image_poll_interval,
        )
        workflow = SongWorkflow(
            memory_root=memory_root,
            prompt_root=prompt_root,
            llm_client=llm_client,
            image_backend=image_backend,
        )
        if args.hitl:
            result = workflow.run_with_hitl(
                book_slug=args.book,
                spoiler_mode=args.spoiler_mode,
                prompt_type=args.prompt_type,
                platform=args.platform,
            )
        else:
            result = workflow.run(
                book_slug=args.book,
                spoiler_mode=args.spoiler_mode,
                prompt_type=args.prompt_type,
                platform=args.platform,
            )

    pprint(result)
    if args.export:
        exported_paths = ExportService(output_root=Path(args.output_root)).export(
            workflow_name=args.command,
            item_slug=args.book,
            data=result,
            formats=args.export,
        )
        pprint({"exports": exported_paths})
    return 0


def _run_hitl_command(args: argparse.Namespace) -> int:
    storage = HITLSessionStorage()
    session = storage.load(args.file)

    if args.hitl_command == "show":
        pprint(session.to_dict())
        return 0

    if args.hitl_command == "approve":
        session.approve_step(args.step, comment=args.comment)
    elif args.hitl_command == "reject":
        session.reject_step(args.step, comment=args.comment)
    elif args.hitl_command == "edit":
        session.edit_step(args.step, edited_content=args.content, comment=args.comment)
    else:  # pragma: no cover
        raise ValueError(f"Unknown HITL command: {args.hitl_command}")

    storage.save_to_path(session, args.file)
    pprint(session.to_dict())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
