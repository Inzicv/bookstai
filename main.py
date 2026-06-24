"""Main CLI entrypoint for BookstAI's local Markdown book manager."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.generators.markdown_generator import clean_filename, create_empty_book_template
from src.services.book_search_service import BookSearchService
from src.services.review_assistant_service import ReviewAssistantService


def ask_text(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def ask_multiline(prompt: str) -> str:
    print(f"{prompt} (ligne vide pour terminer) :")
    lines: list[str] = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines).strip()


def ask_choice(prompt: str, choices: dict[str, str], default_key: str) -> str:
    print(prompt)
    for key, label in choices.items():
        marker = " (dÃ©faut)" if key == default_key else ""
        print(f"  {key}. {label}{marker}")
    value = input("Choix: ").strip() or default_key
    return value if value in choices else default_key


def ensure_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def import_markdown(source_path: str, output_dir: str = "memory/books") -> str:
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Fichier introuvable: {source_path}")
    if source.suffix.lower() != ".md":
        raise ValueError("Le fichier source doit Ãªtre un Markdown (.md).")

    ensure_output_dir(output_dir)
    target_name = clean_filename(source.stem) + ".md"
    target_path = Path(output_dir) / target_name
    shutil.copyfile(source, target_path)
    return str(target_path.resolve())


def create_template(title: str, output_dir: str = "memory/books") -> str:
    ensure_output_dir(output_dir)
    return create_empty_book_template(title, output_dir=output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="BookstAI - gestion locale de fiches livres Markdown."
    )
    parser.add_argument(
        "--output-dir",
        default="memory/books",
        help="RÃ©pertoire de sortie pour les fiches Markdown.",
    )
    parser.add_argument(
        "--source",
        help="Chemin vers un fichier .md existant Ã  importer.",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="CrÃ©e un template vide au lieu d'importer un fichier existant.",
    )
    parser.add_argument(
        "--title",
        help="Titre Ã  utiliser pour le nom de fichier quand on crÃ©e un template.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("search", help="Recherche locale dans les fiches Markdown.")
    subparsers.add_parser("index", help="Reconstruit l'index local des fiches Markdown.")
    subparsers.add_parser(
        "memory",
        help="Indexe les fiches puis affiche les rÃ©sultats pertinents avec leurs sections.",
    )
    review_parser = subparsers.add_parser(
        "review",
        help="Prépare un brouillon de review humoristique pour une fiche active.",
    )
    review_parser.add_argument(
        "--book",
        required=False,
        help="Chemin vers la fiche Markdown active.",
    )
    review_parser.add_argument(
        "--notes",
        help="Notes brutes de l'utilisateur pour l'avis.",
    )
    review_parser.add_argument(
        "--output",
        help="Chemin optionnel pour enregistrer le brouillon.",
    )
    context_parser = subparsers.add_parser(
        "context",
        help="Charge une fiche active et exporte son contexte prêt pour assistant.",
    )
    context_parser.add_argument(
        "--book",
        help="Chemin vers la fiche Markdown active.",
    )
    context_parser.add_argument(
        "--export",
        help="Chemin du fichier de sortie de contexte.",
    )

    args = parser.parse_args()

    try:
        if args.command == "index":
            service = BookSearchService(books_dir=args.output_dir)
            count = service.index_books()
            print(f"\n[Succès] Index reconstruit pour {count} fiche(s).")
            return

        if args.command == "search":
            query = args.title or ask_text("Requête de recherche")
            service = BookSearchService(books_dir=args.output_dir)
            results = service.search(query)
            if not results:
                print("\n[Aucun résultat]")
                return
            print()
            for result in results:
                print(f"- {result.title}")
                print(f"  {result.path}")
                print(f"  score={result.score}")
                print(f"  {result.snippet}")
                print()
            return

        if args.command == "memory":
            query = args.title or ask_text("Requête mémoire")
            service = BookSearchService(books_dir=args.output_dir)
            count = service.index_books()
            print(f"\n[Index] {count} fiche(s) indexée(s).")
            results = service.memory_search(query)
            if not results:
                print("\n[Aucun résultat]")
                return
            print()
            for result, hits in results:
                print(f"- {result.title}")
                print(f"  {result.path}")
                print(f"  score={result.score}")
                print(f"  {result.snippet}")
                for hit in hits[:3]:
                    print(f"    · {hit.section} (score={hit.score})")
                    print(f"      {hit.content}")
                print()
            return

        if args.command == "review":
            book_path = args.book or ask_text(
                "Chemin de la fiche Markdown active",
                "memory/books/lesheritiersdorion.md",
            )
            assistant = ReviewAssistantService(book_path=book_path)
            draft = assistant.build_draft(user_notes=args.notes or "")

            print(f"\n[Book] {draft.book_title}\n")

            print("=== ÉTAPE 1 — Proposition de pitch ===")
            print(draft.pitch_proposal)
            print()
            print("Idées pour travailler le pitch :")
            for item in draft.pitch_ideas:
                print(f"- {item}")
            print()
            pitch_final = ask_multiline(
                "Colle ici ton pitch validé/corrigé, ou laisse vide pour garder la proposition"
            )
            if not pitch_final:
                pitch_final = draft.pitch_proposal

            print("\n=== ÉTAPE 2 — Saisie de l'avis brut ===")
            user_notes = ask_multiline("Colle ici ton avis brut")
            if not user_notes:
                user_notes = args.notes or ""

            draft = assistant.build_draft(user_notes=user_notes)
            print("\n=== Proposition d'avis ===")
            print(draft.avis_proposal)
            print()
            avis_final = ask_multiline(
                "Colle ici ton avis validé/corrigé, ou laisse vide pour garder la proposition"
            )
            if not avis_final:
                avis_final = draft.avis_proposal

            print("\n=== ÉTAPE 3 — Hooks proposés ===")
            for item in draft.hook_suggestions:
                print(f"- {item}")
            print()
            hook_final = ask_text(
                "Choisis ou réécris le hook final",
                draft.hook_suggestions[0] if draft.hook_suggestions else "",
            )

            final_script = "\n".join(
                [
                    f"# {draft.book_title}",
                    "",
                    "## Accroche",
                    draft.style_anchors[0] if draft.style_anchors else "",
                    "",
                    "## Hook",
                    hook_final,
                    "",
                    "## Pitch",
                    pitch_final,
                    "",
                    "## Avis",
                    avis_final,
                    "",
                ]
            ).rstrip() + "\n"

            print("\n=== SCRIPT FINAL ===\n")
            print(final_script)
            if args.output:
                Path(args.output).write_text(final_script, encoding="utf-8")
                print(f"[Export] Brouillon écrit dans : {Path(args.output).resolve()}")
            return

        if args.command == "context":
            book_path = args.book or ask_text("Chemin de la fiche Markdown active")
            service = BookSearchService(books_dir=args.output_dir)
            context = service.load_book_context(book_path)
            print(f"\n[Fiche chargée] {context.title}")
            print()
            for section_name, section_content in context.sections.items():
                print(f"## {section_name}")
                print(section_content)
                print()
            if args.export:
                output_path = service.export_context(book_path, output_path=args.export)
                print(f"[Export] Contexte écrit dans : {output_path}")
            return

        if args.source:
            output_path = import_markdown(args.source, output_dir=args.output_dir)
        else:
            mode = "template" if args.template else ask_choice(
                "Que veux-tu faire ?",
                {
                    "1": "Importer un fichier Markdown existant",
                    "2": "Créer un template vide",
                },
                default_key="1",
            )

            if mode == "2":
                title = args.title or ask_text("Titre du livre")
                output_path = create_template(title, output_dir=args.output_dir)
            else:
                source_path = ask_text("Chemin du fichier Markdown du livre")
                output_path = import_markdown(source_path, output_dir=args.output_dir)

        print(f"\n[Succès] Fiche disponible : {output_path}")
    except KeyboardInterrupt:
        print("\n[Annulé] Opération interrompue par l'utilisateur.", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"\n[Erreur] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
