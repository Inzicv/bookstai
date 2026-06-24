"""Local Review Assistant helper for a single active book.

The logic is intentionally split into small callable steps so it can be reused
from the CLI, tests, a future GUI, or a Langflow workflow.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReviewAssets:
    book_title: str
    book_fields: dict[str, str]
    previous_pitch: list[str]
    previous_avis: list[str]
    humor_refs: list[str]
    pitch_anchor: str
    avis_anchor: str


@dataclass
class StepOutput:
    """Standard output wrapper for Langflow-friendly orchestration."""

    step_name: str
    title: str
    content: str
    options: list[str]
    notes: list[str]


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
    """Builds review drafting assets from the active book and memory files."""

    def __init__(
        self,
        book_path: str,
        reviews_path: str = "memory/reviews/reviews.md",
        humor_path: str = "memory/humor/references.md",
    ) -> None:
        self.book_path = Path(book_path)
        self.reviews_path = Path(reviews_path)
        self.humor_path = Path(humor_path)

    def load_assets(self) -> ReviewAssets:
        book_content = self.book_path.read_text(encoding="utf-8")
        book_title = extract_title(book_content, self.book_path.stem)
        book_fields = extract_book_fields(book_content)
        previous_reviews = extract_review_blocks(self.reviews_path.read_text(encoding="utf-8"))
        humor_refs = load_humor_references(str(self.humor_path))
        pitch_anchor = first_nonempty_line(previous_reviews["pitch"], "Un pitch direct et mordant.")
        avis_anchor = first_nonempty_line(previous_reviews["avis"], "Un avis très incarné et subjectif.")
        return ReviewAssets(
            book_title=book_title,
            book_fields=book_fields,
            previous_pitch=previous_reviews["pitch"],
            previous_avis=previous_reviews["avis"],
            humor_refs=humor_refs,
            pitch_anchor=pitch_anchor,
            avis_anchor=avis_anchor,
        )

    def propose_pitch(self, assets: ReviewAssets) -> str:
        return self._make_pitch_proposal(assets)

    def propose_pitch_step(self, assets: ReviewAssets) -> StepOutput:
        return StepOutput(
            step_name="pitch",
            title=f"Proposition de pitch — {assets.book_title}",
            content=self.propose_pitch(assets),
            options=self.propose_pitch_ideas(assets),
            notes=[
                "L'utilisateur corrige ou conserve la proposition.",
                "Human In The Loop avant de passer à l'avis.",
            ],
        )

    def propose_avis(self, assets: ReviewAssets, user_notes: str) -> str:
        return self._make_avis_proposal(user_notes, assets.avis_anchor, assets.previous_avis)

    def propose_avis_step(self, assets: ReviewAssets, user_notes: str) -> StepOutput:
        return StepOutput(
            step_name="avis",
            title=f"Proposition d'avis — {assets.book_title}",
            content=self.propose_avis(assets, user_notes),
            options=[
                "Remettre les idées dans l'ordre.",
                "Conserver le ton direct des anciens avis.",
                "Garder les émotions de l'utilisateur intactes.",
            ],
            notes=[
                "L'utilisateur saisit son avis brut.",
                "Puis il corrige la proposition avant de passer aux hooks.",
            ],
        )

    def propose_hooks(self, assets: ReviewAssets) -> list[str]:
        return [
            f"Hook 1 : {self._style_hook(assets.book_title, assets.humor_refs, 0, 'un livre qui te chope par le col dès l’ouverture')}",
            f"Hook 2 : {self._style_hook(assets.book_title, assets.humor_refs, 1, 'un roman qui te fait rire avant de te casser le cœur')}",
            f"Hook 3 : {self._style_hook(assets.book_title, assets.humor_refs, 2, 'une lecture qui a la politesse d’être dangereusement addictive')}",
        ]

    def propose_hooks_step(self, assets: ReviewAssets) -> StepOutput:
        hooks = self.propose_hooks(assets)
        return StepOutput(
            step_name="hooks",
            title=f"Propositions de hooks — {assets.book_title}",
            content="\n".join(f"- {hook}" for hook in hooks),
            options=hooks,
            notes=[
                "L'utilisateur choisit ou réécrit le hook final.",
                "Dernière validation humaine avant assemblage.",
            ],
        )

    def propose_pitch_ideas(self, assets: ReviewAssets) -> list[str]:
        resume = self._book_resume(assets.book_fields)
        tropes = (assets.book_fields.get("Tropes", "") or "").replace("\n", " ").strip()
        scenes = (assets.book_fields.get("Scènes importantes", "") or "").replace("\n", " ").strip()
        refs = assets.humor_refs[:3] or ["Référence humoristique à placer au moment du script."]
        return [
            f"Commencer très oral, puis resserrer autour du résumé : {resume[:160].rstrip()}",
            f"Faire ressortir le trope dominant : {tropes[:140].rstrip()}",
            f"Terminer sur une scène forte qui laisse une vraie image : {scenes[:140].rstrip()}",
            f"Ajouter une référence d'humour mémoire : {refs[0]}",
        ]

    def assemble_script(
        self,
        assets: ReviewAssets,
        pitch_final: str,
        avis_final: str,
        hook_final: str,
        user_notes: str,
    ) -> str:
        lines = [f"# {assets.book_title}", ""]
        lines.append("## Accroche")
        lines.append(assets.pitch_anchor)
        lines.append("")
        lines.append("## Hook")
        lines.append(hook_final)
        lines.append("")
        lines.append("## Pitch")
        lines.append(pitch_final)
        lines.append("")
        lines.append("*Ancien résumé mémoire :*")
        lines.append(self._book_resume(assets.book_fields))
        lines.append("")
        lines.append("## Avis")
        lines.append(assets.avis_anchor)
        lines.append("")
        lines.append(avis_final)
        lines.append("")
        lines.append("*Avis brut saisi par l'utilisateur :*")
        lines.append(user_notes.strip() or "*L'utilisateur doit donner son avis brut.*")
        lines.append("")
        lines.append("## Références mémoire")
        lines.append("")
        lines.append("### Reviews précédentes (#pitch)")
        lines.extend(f"- {line}" for line in assets.previous_pitch or ["*Aucune référence trouvée.*"])
        lines.append("")
        lines.append("### Reviews précédentes (#avis)")
        lines.extend(f"- {line}" for line in assets.previous_avis or ["*Aucune référence trouvée.*"])
        lines.append("")
        lines.append("### Références humoristiques")
        lines.extend(f"- {ref}" for ref in assets.humor_refs or ["*Aucune référence trouvée.*"])
        return "\n".join(lines).rstrip() + "\n"

    def assemble_script_step(
        self,
        assets: ReviewAssets,
        pitch_final: str,
        avis_final: str,
        hook_final: str,
        user_notes: str,
    ) -> StepOutput:
        script = self.assemble_script(
            assets=assets,
            pitch_final=pitch_final,
            avis_final=avis_final,
            hook_final=hook_final,
            user_notes=user_notes,
        )
        return StepOutput(
            step_name="assemble",
            title=f"Script final — {assets.book_title}",
            content=script,
            options=[],
            notes=[
                "Résultat final après validation humaine.",
                "Peut être exporté tel quel dans un fichier Markdown.",
            ],
        )

    def build_draft(self, user_notes: str = "") -> ReviewDraft:
        assets = self.load_assets()
        pitch_proposal = self.propose_pitch(assets)
        avis_proposal = self.propose_avis(assets, user_notes)
        pitch_ideas = self.propose_pitch_ideas(assets)
        hook_suggestions = self.propose_hooks(assets)
        final_script = self.assemble_script(
            assets=assets,
            pitch_final=pitch_proposal,
            avis_final=avis_proposal,
            hook_final=hook_suggestions[0] if hook_suggestions else "",
            user_notes=user_notes,
        )
        return ReviewDraft(
            book_title=assets.book_title,
            pitch_proposal=pitch_proposal,
            avis_proposal=avis_proposal,
            hook_suggestions=hook_suggestions,
            pitch_ideas=pitch_ideas,
            style_anchors=[assets.pitch_anchor, assets.avis_anchor],
            final_script=final_script,
        )

    def _book_resume(self, book_fields: dict[str, str]) -> str:
        return (book_fields.get("Résumé", "") or book_fields.get("Résumé spoiler-free", "")).replace("\n", " ").strip()

    def _style_hook(self, book_title: str, refs: list[str], index: int, fallback: str) -> str:
        ref = refs[index] if len(refs) > index else fallback
        return f"{book_title} — {ref}"

    def _make_pitch_proposal(self, assets: ReviewAssets) -> str:
        resume = self._book_resume(assets.book_fields)
        tropes = (assets.book_fields.get("Tropes", "") or "").replace("\n", " ").strip()
        scene = (assets.book_fields.get("Scènes importantes", "") or "").replace("\n", " ").strip()
        ref = assets.humor_refs[0] if assets.humor_refs else "Référence humoristique à caler au moment du script."
        return (
            f"{assets.book_title} ? "
            f"On est sur {resume[:120].rstrip()} "
            f"mais avec le genre de ton qui fait qu'on ne raconte pas juste l'histoire, on la secoue un peu. "
            f"Le trope qui ressort le plus : {tropes[:100].rstrip()}. "
            f"Et la scène qui donne du sel : {scene[:100].rstrip()}. "
            f"On garde le rythme du style mémoire : {assets.pitch_anchor}. "
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
