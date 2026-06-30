"""Tests for HITL sessions."""

from bookstai.core.errors import HITLStepNotFoundError
from bookstai.hitl.models import HITLStatus
from bookstai.hitl.session import HITLSession


def test_hitl_session_keeps_workflow_and_item_slug() -> None:
    session = HITLSession(workflow_name="review", item_slug="lesheritiersdorion")

    assert session.workflow_name == "review"
    assert session.item_slug == "lesheritiersdorion"


def test_add_step_adds_pending_step() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")

    step = session.add_step(name="comedy", content={"response": "..."})

    assert step.status == HITLStatus.PENDING
    assert step.content == {"response": "..."}


def test_get_step_returns_the_correct_step() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")
    session.add_step(name="comedy", content={"response": "..."})

    step = session.get_step("comedy")

    assert step.name == "comedy"


def test_approve_step_sets_approved() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")
    session.add_step(name="comedy", content={"response": "..."})

    step = session.approve_step("comedy")

    assert step.status == HITLStatus.APPROVED


def test_reject_step_sets_rejected_and_keeps_comment() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")
    session.add_step(name="review", content={"response": "..."})

    step = session.reject_step("review", comment="Pas assez drôle.")

    assert step.status == HITLStatus.REJECTED
    assert step.comment == "Pas assez drôle."


def test_edit_step_sets_edited_and_keeps_original_content() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")
    session.add_step(name="social", content="Texte initial")

    step = session.edit_step("social", edited_content="Texte corrigé.")

    assert step.status == HITLStatus.EDITED
    assert step.edited_content == "Texte corrigé."
    assert step.content == "Texte initial"


def test_to_dict_returns_json_serializable_structure() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")
    session.add_step(name="comedy", content={"response": "..."})
    session.approve_step("comedy")

    result = session.to_dict()

    assert result["workflow_name"] == "review"
    assert result["item_slug"] == "example"
    assert result["steps"][0]["status"] == "approved"


def test_missing_step_raises_hitl_step_not_found_error() -> None:
    session = HITLSession(workflow_name="review", item_slug="example")

    for method_name in ["get_step", "approve_step", "reject_step", "edit_step"]:
        method = getattr(session, method_name)
        try:
            if method_name == "edit_step":
                method("missing", edited_content="x")
            else:
                method("missing")
            assert False, "HITLStepNotFoundError expected"
        except HITLStepNotFoundError as exc:
            assert "HITL step 'missing' was not found." == str(exc)
