"""Orchestrator service for BookstAI Librarian V1 pipeline."""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.models.book import BookMemory
from src.extractors.epub_loader import load_epub
from src.generators.markdown_generator import generate_markdown


class LibrarianService:
    """Service orchestrating EPUB loading, Gemini metadata extraction, and markdown generation."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initializes the service and the Gemini client.

        Args:
            model_name: The Gemini model to use for extraction.
        """
        # Load environment variables (e.g. GEMINI_API_KEY)
        load_dotenv()
        
        # Verify that GEMINI_API_KEY is available
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please configure it in a .env file."
            )
        
        # Initialize the new Google GenAI client
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def _load_prompt(self) -> str:
        """Loads the system instruction prompt from src/prompts/librarian_prompt.md.

        Returns:
            The prompt string.
        """
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "prompts",
            "librarian_prompt.md"
        )
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Librarian prompt file not found at: {prompt_path}")
            
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def process_book(self, epub_path: str, output_dir: str = "memory/books") -> str:
        """Runs the pipeline: extracts EPUB text, calls Gemini to get metadata, generates markdown.

        Args:
            epub_path: Path to the EPUB book.
            output_dir: Directory where the markdown should be saved.

        Returns:
            The path to the generated markdown file.
        """
        if not os.path.exists(epub_path):
            raise FileNotFoundError(f"EPUB file not found at: {epub_path}")

        print(f"[*] Extraction du texte de l'EPUB : {epub_path}...")
        raw_text = load_epub(epub_path)
        print(f"[+] Texte extrait ({len(raw_text)} caractères).")

        print("[*] Chargement du prompt système...")
        system_instruction = self._load_prompt()

        print(f"[*] Appel de l'API Gemini ({self.model_name}) pour l'analyse...")
        
        # Call Gemini using the structured output functionality
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"Voici le texte complet du livre :\n\n{raw_text}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=BookMemory,
                temperature=0.2,
            ),
        )

        # Parse the response text as BookMemory
        try:
            # Under the hood, genai SDK parses structured output schema into a Pydantic object
            # or we can parse it from response.text using BookMemory.model_validate_json()
            if not response.text:
                raise ValueError("L'API Gemini a retourné une réponse vide.")
            
            book_memory = BookMemory.model_validate_json(response.text)
        except Exception as e:
            print(f"[-] Erreur lors du parsing JSON de la réponse Gemini : {e}")
            print(f"Texte brut reçu :\n{response.text}")
            raise

        print(f"[+] Analyse terminée. Titre extrait : '{book_memory.title}' par {book_memory.author}.")
        print("[*] Génération du fichier Markdown...")
        md_file_path = generate_markdown(book_memory, output_dir=output_dir)
        print(f"[+] Fichier créé avec succès : {md_file_path}")

        return md_file_path
