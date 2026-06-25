"""Local Review Assistant helper for a single active book.

The logic is intentionally split into small callable steps so it can be reused
from the CLI, tests, a future GUI, or a Langflow workflow.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

try:
    from google import genai
except Exception:  # pragma: no cover - optional dependency
    genai = None


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


class ReviewLLMClient:
    """Optional Gemini client used to generate prose from local Markdown context."""

    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = model_name or os.getenv("BOOKSTAI_REVIEW_MODEL", "gemini-2.5-flash")
        self.enabled = bool(self.api_key and genai is not None)
        self._client = genai.Client(api_key=self.api_key) if self.enabled else None

    def generate_text(self, prompt: str, system_instruction: str) -> str | None:
        if not self.enabled or self._client is None:
            return None
        response = self._client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.7,
            },
        )
        text = getattr(response, "text", None)
        return text.strip() if isinstance(text, str) and text.strip() else None


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_marks = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", without_marks).strip().lower()


def parse_markdown_sections(content: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_name = "Front matter"
    sections[current_name] = []

    for line in content.splitlines():
        match = re.match(r"^#{1,6}\s+(.+)$", line.strip())
        if match:
            current_name = re.sub(r"^\d+[\s\.\-\)]*", "", match.group(1).strip())
            sections.setdefault(current_name, [])
            continue
        sections.setdefault(current_name, []).append(line)

    return {name: "\n".join(lines).strip() for name, lines in sections.items() if "\n".join(lines).strip()}


def pick_section(sections: dict[str, str], wanted: str) -> str:
    wanted_norm = normalize_text(wanted)
    aliases = {
        "résumé": ["résumé", "résumé du tome", "résumé spoiler-free"],
        "tropes": ["tropes", "tropes littéraires"],
        "personnages": [
            "personnages",
            "personnages principaux",
            "personnages (nom, prénom & description physique)",
        ],
        "scènes importantes": ["scènes importantes", "scenes importantes"],
    }
    for section_name, content in sections.items():
        section_norm = normalize_text(section_name)
        if section_norm == wanted_norm:
            return content
        for alias in aliases.get(wanted, [wanted]):
            if section_norm == normalize_text(alias):
                return content
    return ""


def extract_title(content: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def extract_book_fields(content: str) -> dict[str, str]:
    sections = parse_markdown_sections(content)
    fields: dict[str, str] = {}
    for label in ["Résumé", "Résumé spoiler-free", "Tropes", "Personnages", "Scènes importantes"]:
        fields[label] = pick_section(sections, label)
    return fields


def extract_review_blocks(content: str) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {"pitch": [], "avis": []}
    current = None
    for line in content.splitlines():
        stripped = normalize_text(line)
        if stripped in {"#pitch", "## pitch", "pitch"}:
            current = "pitch"
            continue
        if stripped in {"#avis", "## avis", "avis"}:
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


def debug_book_context(
    book_path: str,
    reviews_path: str = "memory/reviews/reviews.md",
    humor_path: str = "memory/humor/references.md",
) -> dict[str, object]:
    """Return a compact debug snapshot for the active book and memory files."""
    book_content = Path(book_path).read_text(encoding="utf-8")
    book_title = extract_title(book_content, Path(book_path).stem)
    sections = parse_markdown_sections(book_content)
    fields = extract_book_fields(book_content)
    previous_reviews = extract_review_blocks(Path(reviews_path).read_text(encoding="utf-8"))
    humor_refs = load_humor_references(humor_path)
    summary_text = fields.get("Résumé", "") or fields.get("Résumé spoiler-free", "")
    return {
        "book_title": book_title,
        "sections_detected": list(sections.keys()),
        "summary_length": len(summary_text),
        "tropes_count": len([line for line in fields.get("Tropes", "").splitlines() if line.strip()]),
        "scenes_count": len([line for line in fields.get("Scènes importantes", "").splitlines() if line.strip()]),
        "pitch_count": len(previous_reviews["pitch"]),
        "avis_count": len(previous_reviews["avis"]),
        "pitch_preview": first_nonempty_line(previous_reviews["pitch"], ""),
        "avis_preview": first_nonempty_line(previous_reviews["avis"], ""),
        "humor_count": len(humor_refs),
        "humor_preview": humor_refs[:5],
        "field_keys": list(fields.keys()),
    }


class ReviewAssistantService:
    """Builds review drafting assets from the active book and memory files."""

    def __init__(
        self,
        book_path: str,
        reviews_path: str = "memory/reviews/reviews.md",
        humor_path: str = "memory/humor/references.md",
        api_key: str | None = None,
        model_name: str | None = None,
    ) -> None:
        self.book_path = Path(book_path)
        self.reviews_path = Path(reviews_path)
        self.humor_path = Path(humor_path)
        self.llm = ReviewLLMClient(api_key=api_key, model_name=model_name)

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
        llm_text = self._generate_pitch_with_llm(assets)
        return llm_text or self._make_pitch_proposal(assets)

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
        llm_text = self._generate_avis_with_llm(assets, user_notes)
        return llm_text or self._make_avis_proposal(user_notes, assets.avis_anchor, assets.previous_avis)

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
        llm_hooks = self._generate_hooks_with_llm(assets)
        if llm_hooks:
            return llm_hooks
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

    def _generate_pitch_with_llm(self, assets: ReviewAssets) -> str | None:
        prompt = "\n".join(
            [
                f"Livre: {assets.book_title}",
                f"Résumé: {self._book_resume(assets.book_fields)}",
                f"Tropes: {(assets.book_fields.get('Tropes', '') or '').replace(chr(10), ' ')}",
                f"Scènes importantes: {(assets.book_fields.get('Scènes importantes', '') or '').replace(chr(10), ' ')}",
                f"Ancien pitch style: {assets.pitch_anchor}",
                f"Références humour: {', '.join(assets.humor_refs[:5])}",
                "",
                "Écris une proposition de pitch en français, orale, drôle, fidèle au ton des reviews existantes.",
                "Retourne uniquement le texte du pitch, sans titre ni puces.",
            ]
        )
        return self.llm.generate_text(
            prompt=prompt,
            system_instruction="Tu es un assistant d'écriture de reviews humoristiques. Tu restes fidèle au ton de l'utilisatrice.",
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

    def _generate_avis_with_llm(self, assets: ReviewAssets, user_notes: str) -> str | None:
        prompt = "\n".join(
            [
                f"Livre: {assets.book_title}",
                f"Avis brut utilisateur: {user_notes.strip() or 'N/A'}",
                f"Ancien avis style: {first_nonempty_line(assets.previous_avis, assets.avis_anchor)}",
                "",
                "Réécris l'avis brut dans un style naturel, direct, incarné et humoristique.",
                "Conserve les émotions de l'utilisateur et n'invente pas d'opinion non présente.",
                "Retourne uniquement le texte de l'avis, sans titre ni puces.",
            ]
        )
        return self.llm.generate_text(
            prompt=prompt,
            system_instruction="Tu réécris des avis de lecture avec une voix très personnelle, vive et humoristique.",
        )

    def _generate_hooks_with_llm(self, assets: ReviewAssets) -> list[str] | None:
        prompt = "\n".join(
            [
                f"Livre: {assets.book_title}",
                f"Résumé: {self._book_resume(assets.book_fields)}",
                f"Humour: {', '.join(assets.humor_refs[:5])}",
                "",
                "Propose 3 hooks courts, percutants, en français.",
                "Chaque hook doit être sur une ligne séparée, sans numérotation, sans explication.",
            ]
        )
        text = self.llm.generate_text(
            prompt=prompt,
            system_instruction="Tu écris des hooks de review très courts, punchy, et adaptés à un public booktok / bookstagram.",
        )
        if not text:
            return None
        hooks = [line.strip("-• \t") for line in text.splitlines() if line.strip()]
        hooks = [hook for hook in hooks if hook]
        return hooks[:3] or None
