"""Tests for the Learning Loop extractor."""

from bookstai.hitl import HITLSession, HITLStatus
from bookstai.learning import LearningExtractor


def test_extract_approved_step_becomes_candidate() -> None:
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="review", content="version IA")
    session.approve_step("review", comment="OK")

    extraction = LearningExtractor().extract(session)

    assert len(extraction.candidates) == 1
    candidate = extraction.candidates[0]
    assert candidate.step_name == "review"
    assert candidate.status == "approved"
    assert candidate.original_content == "version IA"
    assert candidate.validated_content == "version IA"
    assert candidate.edited_content is None
    assert candidate.comment == "OK"


def test_extract_edited_step_becomes_candidate() -> None:
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="social", content="Texte original")
    session.edit_step("social", edited_content="Texte corrigé", comment="Plus naturel")

    extraction = LearningExtractor().extract(session)

    assert len(extraction.candidates) == 1
    candidate = extraction.candidates[0]
    assert candidate.step_name == "social"
    assert candidate.status == "edited"
    assert candidate.original_content == "Texte original"
    assert candidate.validated_content == "Texte corrigé"
    assert candidate.edited_content == "Texte corrigé"
    assert candidate.comment == "Plus naturel"


def test_extract_edited_step_without_value_is_ignored() -> None:
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="social", content="Texte original")
    step = session.get_step("social")
    step.status = HITLStatus.EDITED

    extraction = LearningExtractor().extract(session)

    assert extraction.candidates == []
    assert extraction.pending_steps == ["social"]


def test_extract_rejected_step_is_tracked_not_candidate() -> None:
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="social", content="Texte original")
    session.reject_step("social", comment="Pas bon")

    extraction = LearningExtractor().extract(session)

    assert extraction.candidates == []
    assert extraction.rejected_steps == ["social"]


def test_extract_pending_step_is_tracked_not_candidate() -> None:
    session = HITLSession(workflow_name="review", item_slug="book")
    session.add_step(name="comedy", content="Brouillon")

    extraction = LearningExtractor().extract(session)

    assert extraction.candidates == []
    assert extraction.pending_steps == ["comedy"]


def test_extract_conserves_metadata_and_dict_output() -> None:
    session = HITLSession(workflow_name="song", item_slug="book")
    session.add_step(name="song", content={"text": "IA"}, metadata={"source": "llm"})
    session.edit_step("song", edited_content={"text": "corrigé"}, comment="Ajusté")

    extraction = LearningExtractor().extract(session)

    assert extraction.workflow_name == "song"
    assert extraction.item_slug == "book"
    assert extraction.candidates[0].metadata == {"source": "llm"}
    assert extraction.to_dict() == {
        "workflow_name": "song",
        "item_slug": "book",
        "candidates": [
            {
                "step_name": "song",
                "status": "edited",
                "original_content": {"text": "IA"},
                "validated_content": {"text": "corrigé"},
                "edited_content": {"text": "corrigé"},
                "comment": "Ajusté",
                "metadata": {"source": "llm"},
            }
        ],
        "rejected_steps": [],
        "pending_steps": [],
    }
