"""Main CLI entrypoint for BookstAI's local Markdown book manager."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.generators.markdown_generator import clean_filename, create_empty_book_template


def ask_text(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def ask_choice(prompt: str, choices: dict[str, str], default_key: str) -> str:
    print(prompt)
    for key, label in choices.items():
        marker = " (défaut)" if key == default_key else ""
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
        raise ValueError("Le fichier source doit être un Markdown (.md).")

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
        help="Répertoire de sortie pour les fiches Markdown.",
    )
    parser.add_argument(
        "--source",
        help="Chemin vers un fichier .md existant à importer.",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Crée un template vide au lieu d'importer un fichier existant.",
    )
    parser.add_argument(
        "--title",
        help="Titre à utiliser pour le nom de fichier quand on crée un template.",
    )

    args = parser.parse_args()

    try:
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
