"""Command-line interface for BookstAI."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from pprint import pprint
from typing import Sequence

from .core.config import load_settings
from .core.errors import BookstAIError
from .exports import ExportService
from .hitl import HITLSessionStorage
from .history import HistoryEntry, HistoryStore
from .learning import (
    LearningDraftApplier,
    LearningDraftWriter,
    LearningExtractor,
)
from .logging import configure_logging
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
    review_parser.add_argument("--verbose", action="store_true")
    review_parser.add_argument("--no-history", action="store_true")
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
    song_parser.add_argument("--hitl", action="store_true")
    song_parser.add_argument("--verbose", action="store_true")
    song_parser.add_argument("--no-history", action="store_true")
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
    hitl_parser.add_argument("--verbose", action="store_true")
    hitl_parser.add_argument("--no-history", action="store_true")

    learning_parser = subparsers.add_parser("learning")
    learning_subparsers = learning_parser.add_subparsers(dest="learning_command", required=True)

    learning_extract_parser = learning_subparsers.add_parser("extract")
    learning_extract_parser.add_argument("--hitl-file", required=True)

    learning_draft_parser = learning_subparsers.add_parser("draft")
    learning_draft_parser.add_argument("--hitl-file", required=True)
    learning_draft_parser.add_argument("--output-root", default="outputs/learning")

    learning_apply_parser = learning_subparsers.add_parser("apply")
    learning_apply_parser.add_argument("--draft-file", required=True)
    learning_apply_parser.add_argument("--memory-file", required=True)
    learning_apply_parser.add_argument("--memory-root", default="memory")
    learning_parser.add_argument("--verbose", action="store_true")
    learning_parser.add_argument("--no-history", action="store_true")

    history_parser = subparsers.add_parser("history")
    history_subparsers = history_parser.add_subparsers(dest="history_command", required=True)
    history_show = history_subparsers.add_parser("show")
    history_show.add_argument("--file", default="outputs/history/bookstai-history.jsonl")
    history_show.add_argument("--verbose", action="store_true")
    history_show.add_argument("--no-history", action="store_true")
    history_tail = history_subparsers.add_parser("tail")
    history_tail.add_argument("--file", default="outputs/history/bookstai-history.jsonl")
    history_tail.add_argument("--limit", type=int, default=10)
    history_tail.add_argument("--verbose", action="store_true")
    history_tail.add_argument("--no-history", action="store_true")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(verbose=getattr(args, "verbose", False))

    history_store = HistoryStore()
    use_history = not getattr(args, "no_history", False)

    try:
        if args.command == "hitl":
            exit_code = _run_hitl_command(args)
            if use_history:
                history_store.append(
                    HistoryEntry(
                        command=f"hitl {args.hitl_command}",
                        status="success",
                        artifacts={"file": args.file, "step": getattr(args, "step", None)},
                    )
                )
            return exit_code

        if args.command == "learning":
            exit_code = _run_learning_command(args)
            if use_history:
                artifacts = {"hitl_file": getattr(args, "hitl_file", None)}
                if args.learning_command == "draft":
                    artifacts["draft_path"] = getattr(args, "_learning_draft_path", None)
                if args.learning_command == "apply":
                    artifacts = {
                        "draft_file": args.draft_file,
                        "memory_file": args.memory_file,
                        "memory_path": getattr(args, "_memory_path", None),
                        "backup_path": getattr(args, "_backup_path", None),
                    }
                history_store.append(
                    HistoryEntry(
                        command=f"learning {args.learning_command}",
                        status="success",
                        artifacts=artifacts,
                    )
                )
            return exit_code

        if args.command == "history":
            return _run_history_command(args)

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
            workflow = SongWorkflow(
                memory_root=memory_root,
                prompt_root=prompt_root,
                llm_client=llm_client,
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
        exported_paths = None
        if args.export:
            exported_paths = ExportService(output_root=Path(args.output_root)).export(
                workflow_name=args.command,
                item_slug=args.book,
                data=result,
                formats=args.export,
            )
            pprint({"exports": exported_paths})
        if use_history:
            history_store.append(
                HistoryEntry(
                    command=args.command,
                    status="success",
                    workflow_name=args.command,
                    item_slug=args.book,
                    hitl_enabled=args.hitl,
                    provider=args.provider,
                    artifacts={
                        "exports": {k: str(v) for k, v in (exported_paths or {}).items()},
                        "has_hitl": "hitl" in result,
                    },
                )
            )
        return 0
    except BookstAIError as exc:
        print(f"BookstAI error: {exc}")
        if use_history:
            history_store.append(
                HistoryEntry(
                    command=args.command,
                    status="failed",
                    workflow_name=getattr(args, "command", None) if args.command in {"review", "song"} else None,
                    item_slug=getattr(args, "book", None),
                    hitl_enabled=getattr(args, "hitl", False),
                    provider=getattr(args, "provider", None),
                    error=str(exc),
                )
            )
        return 1


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


def _run_learning_command(args: argparse.Namespace) -> int:
    if args.learning_command == "extract":
        session = HITLSessionStorage().load(args.hitl_file)
        extraction = LearningExtractor().extract(session)
        pprint(extraction.to_dict() if hasattr(extraction, "to_dict") else extraction)
        args._learning_draft_path = None
        return 0

    if args.learning_command == "draft":
        session = HITLSessionStorage().load(args.hitl_file)
        extraction = LearningExtractor().extract(session)
        path = LearningDraftWriter(output_root=args.output_root).write(extraction)
        args._learning_draft_path = path
        pprint({"learning_draft": str(path)})
        return 0

    if args.learning_command == "apply":
        result = LearningDraftApplier(memory_root=args.memory_root).apply(
            draft_path=args.draft_file,
            memory_file=args.memory_file,
        )
        args._memory_path = result.memory_path
        args._backup_path = result.backup_path
        pprint(
            {
                "draft_path": str(result.draft_path),
                "memory_path": str(result.memory_path),
                "backup_path": str(result.backup_path) if result.backup_path else None,
                "applied": result.applied,
            }
        )
        return 0

    raise ValueError(f"Unknown learning command: {args.learning_command}")


def _run_history_command(args: argparse.Namespace) -> int:
    store = HistoryStore(args.file)
    if args.history_command == "show":
        pprint(store.read_all())
        return 0
    if args.history_command == "tail":
        pprint(store.tail(limit=args.limit))
        return 0
    raise ValueError(f"Unknown history command: {args.history_command}")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
