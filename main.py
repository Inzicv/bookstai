"""Main CLI entrypoint for BookstAI Librarian V1."""

import os
import sys
import argparse

# Add current folder to path to make src imports work nicely
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.librarian_service import LibrarianService


def main() -> None:
    """Parses command-line arguments and runs the Librarian pipeline."""
    parser = argparse.ArgumentParser(
        description="BookstAI Librarian V1 - Extrait de façon structurée les informations clés d'un EPUB."
    )
    parser.add_argument(
        "epub_path",
        help="Chemin vers le fichier EPUB à traiter."
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="Nom du modèle Gemini à utiliser (défaut: gemini-2.5-flash)."
    )
    parser.add_argument(
        "--output-dir",
        default="memory/books",
        help="Répertoire de sortie pour le fichier Markdown (défaut: memory/books)."
    )

    args = parser.parse_args()

    try:
        service = LibrarianService(model_name=args.model)
        output_path = service.process_book(
            epub_path=args.epub_path,
            output_dir=args.output_dir
        )
        print(f"\n[Succès] Pipeline exécuté avec succès. Fiche livre générée : {output_path}")
    except Exception as e:
        print(f"\n[Erreur] L'exécution du pipeline a échoué : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
