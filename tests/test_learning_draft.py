"""Tests for Learning Loop draft writing."""

from __future__ import annotations

from pathlib import Path

from bookstai.learning import LearningCandidate, LearningDraftWriter, LearningExtraction


def test_draft_writer_creates_root_directory(tmp_path) -> None:
    root = tmp_path / "learning"

    writer = LearningDraftWriter(output_root=root)

    assert root.exists()
    assert root.is_dir()
    assert writer.output_root == root


def test_write_creates_markdown_file_and_returns_path(tmp_path) -> None:
    writer = LearningDraftWriter(output_root=tmp_path / "learning")
    extraction = LearningExtraction(
        workflow_name="review",
        item_slug="lesheritiersdorion",
        candidates=[
            LearningCandidate(
                step_name="review",
                status="edited",
                original_content="version IA",
                validated_content="version corrigée",
                edited_content="version corrigée",
                comment="Plus naturel",
            )
        ],
        rejected_steps=["social"],
        pending_steps=["comedy"],
    )

    path = writer.write(extraction)

    assert path.exists()
    assert path.name == "lesheritiersdorion-learning-draft.md"
    assert path.parent.name == "review"


def test_write_includes_expected_sections(tmp_path) -> None:
    writer = LearningDraftWriter(output_root=tmp_path / "learning")
    extraction = LearningExtraction(
        workflow_name="song",
        item_slug="book",
        candidates=[
            LearningCandidate(
                step_name="song",
                status="approved",
                original_content="Texte IA",
                validated_content="Texte IA",
                comment="",
            )
        ],
        rejected_steps=["image"],
        pending_steps=["social"],
    )

    content = writer.write(extraction).read_text(encoding="utf-8")

    assert "Learning Draft - song / book" in content
    assert "## Contexte" in content
    assert "- **Workflow :** song" in content
    assert "- **Livre :** book" in content
    assert "### Étape : song" in content
    assert "- **Statut :** approved" in content
    assert "#### Contenu original" in content
    assert "Texte IA" in content
    assert "#### Contenu validé" in content
    assert "## Étapes rejetées" in content
    assert "- image" in content
    assert "## Étapes en attente" in content
    assert "- social" in content


def test_write_handles_empty_candidates(tmp_path) -> None:
    writer = LearningDraftWriter(output_root=tmp_path / "learning")
    extraction = LearningExtraction(
        workflow_name="review",
        item_slug="book",
        candidates=[],
        rejected_steps=[],
        pending_steps=[],
    )

    content = writer.write(extraction).read_text(encoding="utf-8")

    assert "Aucune candidate d'apprentissage exploitable." in content


def test_write_serializes_dictionary_content(tmp_path) -> None:
    writer = LearningDraftWriter(output_root=tmp_path / "learning")
    extraction = LearningExtraction(
        workflow_name="review",
        item_slug="book",
        candidates=[
            LearningCandidate(
                step_name="review",
                status="edited",
                original_content={"text": "IA"},
                validated_content={"text": "corrigé"},
                edited_content={"text": "corrigé"},
                comment="Ajusté",
            )
        ],
        rejected_steps=[],
        pending_steps=[],
    )

    content = writer.write(extraction).read_text(encoding="utf-8")

    assert '"text": "IA"' in content
    assert '"text": "corrigé"' in content


def test_write_does_not_modify_memory_files(tmp_path) -> None:
    writer = LearningDraftWriter(output_root=tmp_path / "learning")
    extraction = LearningExtraction(
        workflow_name="review",
        item_slug="book",
        candidates=[],
        rejected_steps=[],
        pending_steps=[],
    )

    memory_root = Path("memory")
    before = sorted(str(path) for path in memory_root.rglob("*")) if memory_root.exists() else None
    writer.write(extraction)
    after = sorted(str(path) for path in memory_root.rglob("*")) if memory_root.exists() else None

    assert after == before
