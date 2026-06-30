"""Tests for HITL models."""

from bookstai.hitl.models import HITLStatus, HITLStep


def test_hitl_status_values() -> None:
    assert HITLStatus.PENDING.value == "pending"
    assert HITLStatus.APPROVED.value == "approved"
    assert HITLStatus.REJECTED.value == "rejected"
    assert HITLStatus.EDITED.value == "edited"


def test_hitl_step_defaults_to_pending() -> None:
    step = HITLStep(name="comedy", content={"response": "ok"})

    assert step.status == HITLStatus.PENDING
    assert step.edited_content is None
    assert step.content == {"response": "ok"}


def test_hitl_step_accepts_metadata() -> None:
    step = HITLStep(
        name="social",
        content="caption",
        metadata={"source": "llm"},
    )

    assert step.metadata == {"source": "llm"}


def test_hitl_step_validated_content_pending_returns_content() -> None:
    step = HITLStep(name="social", content="original")

    assert step.validated_content == "original"


def test_hitl_step_validated_content_approved_returns_content() -> None:
    step = HITLStep(name="social", content="original", status=HITLStatus.APPROVED)

    assert step.validated_content == "original"


def test_hitl_step_validated_content_edited_returns_edited_content() -> None:
    step = HITLStep(
        name="social",
        content="original",
        status=HITLStatus.EDITED,
        edited_content="corrected",
    )

    assert step.validated_content == "corrected"


def test_hitl_step_validated_content_edited_without_value_returns_none() -> None:
    step = HITLStep(name="social", content="original", status=HITLStatus.EDITED)

    assert step.validated_content is None


def test_hitl_step_validated_content_rejected_returns_none() -> None:
    step = HITLStep(name="social", content="original", status=HITLStatus.REJECTED)

    assert step.validated_content is None


def test_hitl_step_editing_keeps_original_content() -> None:
    step = HITLStep(name="social", content="original")
    step.edited_content = "corrected"
    step.status = HITLStatus.EDITED

    assert step.content == "original"
