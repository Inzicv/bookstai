"""Local Review Assistant helper for a single active book."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReviewDraft:
    book_title: str
    hook_ideas: list[str]
    pitch_ideas: list[str]
    review_notes: list[str]
    hook_suggestions: list[str]
    final_script: str


def extract_section(content: str, section_name: str) -> str:
    pattern = re.compile(rf"^#+\s+{re.escape(section_name)}\s*$", flags=re.MULTILINE | re.IGNORECASE)
    match = pattern.search(content)
    if not match:
        return ""
    start = match.end()
    next_section = re.search(r"^#+\s+", content[start:], flags=re.MULTILINE)
    end = start + next_section.start() if next_section else len(content)
    return content[start:end].strip()


def extract_title(content: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def extract_book_fields(content: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for label in ["Résumé", "Résumé spoiler-free", "Tropes", "Personnages", "Scènes importantes"]:
        fields[label] = extract_section(content, label)
    return fields


def extract_review_blocks(content: str) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {"pitch": [], "avis": []}
    current = None
    for line in content.splitlines():
        stripped = line.strip().lower()
        if stripped == "#pitch" or stripped == "## pitch":
            current = "pitch"
            continue
        if stripped == "#avis" or stripped == "## avis":
            current = "avis"
            continue
        if current and line.strip():
            blocks[current].append(line.strip())
    return blocks


def load_humor_references(path: str) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[:20]


class ReviewAssistantService:
    """Builds a review drafting brief from the active book and memory files."""

    def __init__(
        self,
        book_path: str,
        reviews_path: str = "memory/reviews/reviews.md",
        humor_path: str = "memory/humor/references.md",
    ) -> None:
        self.book_path = Path(book_path)
        self.reviews_path = Path(reviews_path)
        self.humor_path = Path(humor_path)

    def build_draft(self, user_notes: str = "") -> ReviewDraft:
        book_content = self.book_path.read_text(encoding="utf-8")
        book_title = extract_title(book_content, self.book_path.stem)
        fields = extract_book_fields(book_content)
        previous_reviews = extract_review_blocks(self.reviews_path.read_text(encoding="utf-8"))
        humor_refs = load_humor_references(str(self.humor_path))

        hook_ideas = [
            f"Hook à partir du résumé : {fields['Résumé'][:180].strip()}",
            f"Hook à partir des tropes : {fields['Tropes'][:180].strip()}",
            f"Hook à partir des scènes fortes : {fields['Scènes importantes'][:180].strip()}",
        ]

        pitch_ideas = [
            f"Résumé humoristique à partir du livre actif ({book_title})",
            "Ajouter des analogies, métaphores et comparaisons dans le ton des reviews précédentes.",
            "S'appuyer sur les références d'humour enregistrées.",
        ]

        review_notes = [
            "Étape 1 : proposer plusieurs directions de pitch.",
            "Étape 2 : reformuler l'avis brut de l'utilisateur.",
            "Étape 3 : proposer 2 ou 3 hooks.",
            "Étape 4 : assembler le script final validé par l'utilisateur.",
        ]

        hook_suggestions = [
            f"Suggestion 1 : {humor_refs[0] if humor_refs else 'hook direct et incisif'}",
            f"Suggestion 2 : {humor_refs[1] if len(humor_refs) > 1 else 'hook plus sarcastique'}",
            f"Suggestion 3 : {humor_refs[2] if len(humor_refs) > 2 else 'hook plus émotionnel'}",
        ]

        final_script = self._render_script(
            book_title=book_title,
            fields=fields,
            user_notes=user_notes,
            previous_pitch=previous_reviews["pitch"][:8],
            previous_avis=previous_reviews["avis"][:8],
            humor_refs=humor_refs,
        )

        return ReviewDraft(
            book_title=book_title,
            hook_ideas=hook_ideas,
            pitch_ideas=pitch_ideas,
            review_notes=review_notes,
            hook_suggestions=hook_suggestions,
            final_script=final_script,
        )

    def _render_script(
        self,
        book_title: str,
        fields: dict[str, str],
        user_notes: str,
        previous_pitch: list[str],
        previous_avis: list[str],
        humor_refs: list[str],
    ) -> str:
        lines = [f"# Review draft — {book_title}", ""]
        lines.append("## Hook")
        lines.append("*À valider par l'utilisateur*")
        lines.append("")
        lines.append("## Pitch")
        lines.append(fields.get("Résumé", "") or fields.get("Résumé spoiler-free", ""))
        lines.append("")
        lines.append("## Avis")
        lines.append(user_notes.strip() or "*L'utilisateur doit donner son avis brut.*")
        lines.append("")
        lines.append("## Références mémoire")
        lines.append("")
        lines.append("### Reviews précédentes (#pitch)")
        lines.extend(f"- {line}" for line in previous_pitch or ["*Aucune référence trouvée.*"])
        lines.append("")
        lines.append("### Reviews précédentes (#avis)")
        lines.extend(f"- {line}" for line in previous_avis or ["*Aucune référence trouvée.*"])
        lines.append("")
        lines.append("### Références humoristiques")
        lines.extend(f"- {ref}" for ref in humor_refs or ["*Aucune référence trouvée.*"])
        return "\n".join(lines).rstrip() + "\n"
