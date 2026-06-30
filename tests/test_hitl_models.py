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
