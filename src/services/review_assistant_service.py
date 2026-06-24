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
    style_anchors: list[str]
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


def first_nonempty_line(blocks: list[str], fallback: str) -> str:
    for line in blocks:
        stripped = line.strip()
        if stripped:
            return stripped
    return fallback


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
        pitch_anchor = first_nonempty_line(previous_reviews["pitch"], "Un pitch direct et mordant.")
        avis_anchor = first_nonempty_line(previous_reviews["avis"], "Un avis très incarné et subjectif.")

        hook_ideas = [
            self._make_hook_idea(fields["Résumé"], "résumé"),
            self._make_hook_idea(fields["Tropes"], "tropes"),
            self._make_hook_idea(fields["Scènes importantes"], "scènes fortes"),
        ]

        pitch_ideas = [
            self._make_pitch_idea(book_title, fields, pitch_anchor, humor_refs),
            "Garder le rythme : une phrase d'accroche, une montée en tension, puis une chute qui fait sourire.",
            "Ajouter des analogies et comparaisons très incarnées, comme dans les reviews précédentes.",
        ]

        review_notes = [
            "Étape 1 : proposer plusieurs directions de pitch.",
            "Étape 2 : reformuler l'avis brut de l'utilisateur.",
            "Étape 3 : proposer 2 ou 3 hooks.",
            "Étape 4 : assembler le script final validé par l'utilisateur.",
        ]

        hook_suggestions = [
            f"Hook 1 : {self._style_hook(book_title, humor_refs, 0, 'un livre qui te chope par le col dès l’ouverture')}",
            f"Hook 2 : {self._style_hook(book_title, humor_refs, 1, 'un roman qui te fait rire avant de te casser le cœur')}",
            f"Hook 3 : {self._style_hook(book_title, humor_refs, 2, 'une lecture qui a la politesse d’être dangereusement addictive')}",
        ]

        final_script = self._render_script(
            book_title=book_title,
            fields=fields,
            user_notes=user_notes,
            previous_pitch=previous_reviews["pitch"][:8],
            previous_avis=previous_reviews["avis"][:8],
            humor_refs=humor_refs,
            pitch_anchor=pitch_anchor,
            avis_anchor=avis_anchor,
        )

        return ReviewDraft(
            book_title=book_title,
            hook_ideas=hook_ideas,
            pitch_ideas=pitch_ideas,
            review_notes=review_notes,
            hook_suggestions=hook_suggestions,
            style_anchors=[pitch_anchor, avis_anchor],
            final_script=final_script,
        )

    def _make_hook_idea(self, text: str, label: str) -> str:
        cleaned = text.strip().replace("\n", " ")
        if not cleaned:
            return f"Hook à partir des {label} : trouver l'angle le plus mordant."
        return f"Hook à partir des {label} : {cleaned[:160].rstrip()}"

    def _style_hook(self, book_title: str, refs: list[str], index: int, fallback: str) -> str:
        ref = refs[index] if len(refs) > index else fallback
        return f"{book_title} — {ref}"

    def _make_pitch_idea(self, book_title: str, fields: dict[str, str], pitch_anchor: str, humor_refs: list[str]) -> str:
        resume = (fields.get("Résumé", "") or fields.get("Résumé spoiler-free", "")).replace("\n", " ").strip()
        tropes = (fields.get("Tropes", "") or "").replace("\n", " ").strip()
        scene = (fields.get("Scènes importantes", "") or "").replace("\n", " ").strip()
        ref = humor_refs[0] if humor_refs else "Référence humoristique à caler au moment du script."
        return (
            f"Pitch façon review : {book_title}, version orale et nerveuse. "
            f"Partir du résumé ({resume[:120].rstrip()}) puis enchaîner sur les tropes ({tropes[:100].rstrip()}) "
            f"avec une chute plus personnelle. Ancrage style : {pitch_anchor}. Référence possible : {ref}. "
            f"Si besoin, s’appuyer sur la scène forte suivante : {scene[:100].rstrip()}."
        )

    def _render_script(
        self,
        book_title: str,
        fields: dict[str, str],
        user_notes: str,
        previous_pitch: list[str],
        previous_avis: list[str],
        humor_refs: list[str],
        pitch_anchor: str,
        avis_anchor: str,
    ) -> str:
        lines = [f"# {book_title}", ""]
        lines.append("## Accroche")
        lines.append(pitch_anchor)
        lines.append("")
        lines.append("## Hook")
        lines.append("*Propositions à valider par l'utilisateur*")
        lines.append("")
        lines.append("## Pitch")
        lines.append(fields.get("Résumé", "") or fields.get("Résumé spoiler-free", ""))
        if fields.get("Tropes"):
            lines.append("")
            lines.append(f"*Tropes repérés : {fields['Tropes'].replace(chr(10), ' ')}*")
        if fields.get("Scènes importantes"):
            lines.append("")
            lines.append(f"*Scènes fortes : {fields['Scènes importantes'].replace(chr(10), ' ')}*")
        lines.append("")
        lines.append("## Avis")
        lines.append(avis_anchor)
        lines.append("")
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
