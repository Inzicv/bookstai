"""Tests for Learning Loop models."""

from bookstai.learning import LearningCandidate, LearningExtraction


def test_learning_candidate_conserves_fields() -> None:
    candidate = LearningCandidate(
        step_name="review",
        status="edited",
        original_content="version IA",
        validated_content="version corrigée",
        edited_content="version corrigée",
        comment="Plus naturel",
        metadata={"source": "hitl"},
    )

    assert candidate.step_name == "review"
    assert candidate.status == "edited"
    assert candidate.original_content == "version IA"
    assert candidate.validated_content == "version corrigée"
    assert candidate.edited_content == "version corrigée"
    assert candidate.comment == "Plus naturel"
    assert candidate.metadata == {"source": "hitl"}


def test_learning_extraction_conserves_fields() -> None:
    candidate = LearningCandidate(
        step_name="review",
        status="edited",
        original_content="version IA",
        validated_content="version corrigée",
    )
    extraction = LearningExtraction(
        workflow_name="review",
        item_slug="book",
        candidates=[candidate],
        rejected_steps=["social"],
        pending_steps=["comedy"],
    )

    assert extraction.workflow_name == "review"
    assert extraction.item_slug == "book"
    assert extraction.candidates == [candidate]
    assert extraction.rejected_steps == ["social"]
    assert extraction.pending_steps == ["comedy"]


def test_learning_models_are_json_compatible() -> None:
    candidate = LearningCandidate(
        step_name="review",
        status="approved",
        original_content={"text": "ok"},
        validated_content={"text": "ok"},
    )
    extraction = LearningExtraction(
        workflow_name="review",
        item_slug="book",
        candidates=[candidate],
        rejected_steps=[],
        pending_steps=[],
    )

    assert extraction.to_dict() == {
        "workflow_name": "review",
        "item_slug": "book",
        "candidates": [
            {
                "step_name": "review",
                "status": "approved",
                "original_content": {"text": "ok"},
                "validated_content": {"text": "ok"},
                "edited_content": None,
                "comment": None,
                "metadata": {},
            }
        ],
        "rejected_steps": [],
        "pending_steps": [],
    }
