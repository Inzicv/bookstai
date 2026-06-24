"""Local Review Assistant helper for a single active book."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReviewDraft:
    book_title: str
    pitch_proposal: str
    avis_proposal: str
    hook_suggestions: list[str]
    pitch_ideas: list[str]
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

        pitch_proposal = self._make_pitch_proposal(book_title, fields, pitch_anchor, humor_refs)
        avis_proposal = self._make_avis_proposal(user_notes, avis_anchor, previous_reviews["avis"])
        pitch_ideas = self._make_pitch_ideas(fields, humor_refs)
        hook_suggestions = [
            f"Hook 1 : {self._style_hook(book_title, humor_refs, 0, 'un livre qui te chope par le col dès l’ouverture')}",
            f"Hook 2 : {self._style_hook(book_title, humor_refs, 1, 'un roman qui te fait rire avant de te casser le cœur')}",
            f"Hook 3 : {self._style_hook(book_title, humor_refs, 2, 'une lecture qui a la politesse d’être dangereusement addictive')}",
        ]

        final_script = self._render_script(
            book_title=book_title,
            fields=fields,
            pitch_proposal=pitch_proposal,
            avis_proposal=avis_proposal,
            previous_pitch=previous_reviews["pitch"][:8],
            previous_avis=previous_reviews["avis"][:8],
            humor_refs=humor_refs,
            pitch_anchor=pitch_anchor,
            avis_anchor=avis_anchor,
            user_notes=user_notes,
        )

        return ReviewDraft(
            book_title=book_title,
            pitch_proposal=pitch_proposal,
            avis_proposal=avis_proposal,
            pitch_ideas=pitch_ideas,
            hook_suggestions=hook_suggestions,
            style_anchors=[pitch_anchor, avis_anchor],
            final_script=final_script,
        )

    def _make_pitch_ideas(self, fields: dict[str, str], humor_refs: list[str]) -> list[str]:
        resume = (fields.get("Résumé", "") or fields.get("Résumé spoiler-free", "")).replace("\n", " ").strip()
        tropes = (fields.get("Tropes", "") or "").replace("\n", " ").strip()
        scenes = (fields.get("Scènes importantes", "") or "").replace("\n", " ").strip()
        refs = humor_refs[:3] or ["Référence humoristique à placer au moment du script."]
        return [
            f"Commencer très oral, puis resserrer autour du résumé : {resume[:160].rstrip()}",
            f"Faire ressortir le trope dominant : {tropes[:140].rstrip()}",
            f"Terminer sur une scène forte qui laisse une vraie image : {scenes[:140].rstrip()}",
            f"Ajouter une référence d'humour mémoire : {refs[0]}",
        ]

    def _style_hook(self, book_title: str, refs: list[str], index: int, fallback: str) -> str:
        ref = refs[index] if len(refs) > index else fallback
        return f"{book_title} — {ref}"

    def _make_pitch_proposal(self, book_title: str, fields: dict[str, str], pitch_anchor: str, humor_refs: list[str]) -> str:
        resume = (fields.get("Résumé", "") or fields.get("Résumé spoiler-free", "")).replace("\n", " ").strip()
        tropes = (fields.get("Tropes", "") or "").replace("\n", " ").strip()
        scene = (fields.get("Scènes importantes", "") or "").replace("\n", " ").strip()
        ref = humor_refs[0] if humor_refs else "Référence humoristique à caler au moment du script."
        return (
            f"{book_title} ? "
            f"On est sur {resume[:120].rstrip()} "
            f"mais avec le genre de ton qui fait qu'on ne raconte pas juste l'histoire, on la secoue un peu. "
            f"Le trope qui ressort le plus : {tropes[:100].rstrip()}. "
            f"Et la scène qui donne du sel : {scene[:100].rstrip()}. "
            f"On garde le rythme du style mémoire : {pitch_anchor}. "
            f"Référence utile : {ref}."
        )

    def _make_avis_proposal(self, user_notes: str, avis_anchor: str, previous_avis: list[str]) -> str:
        base = user_notes.strip() or "L'utilisateur doit donner son avis brut."
        sample = first_nonempty_line(previous_avis, avis_anchor)
        return (
            f"{sample}\n\n"
            f"{base}\n\n"
            f"Version lissée : garder ce que l'utilisateur ressent, remettre les idées dans l'ordre, "
            f"et conserver le ton direct et incarné des anciens avis."
        )

    def _render_script(
        self,
        book_title: str,
        fields: dict[str, str],
        pitch_proposal: str,
        avis_proposal: str,
        previous_pitch: list[str],
        previous_avis: list[str],
        humor_refs: list[str],
        pitch_anchor: str,
        avis_anchor: str,
        user_notes: str,
    ) -> str:
        lines = [f"# {book_title}", ""]
        lines.append("## Accroche")
        lines.append(pitch_anchor)
        lines.append("")
        lines.append("## Hook")
        lines.append("*Propositions à valider par l'utilisateur*")
        lines.append("")
        lines.append("## Pitch")
        lines.append(pitch_proposal)
        lines.append("")
        lines.append("*Ancien résumé mémoire :*")
        lines.append(fields.get("Résumé", "") or fields.get("Résumé spoiler-free", ""))
        lines.append("")
        lines.append("## Avis")
        lines.append(avis_anchor)
        lines.append("")
        lines.append(avis_proposal)
        lines.append("")
        lines.append("*Avis brut saisi par l'utilisateur :*")
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
