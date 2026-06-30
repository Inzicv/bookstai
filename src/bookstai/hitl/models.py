"""Human In The Loop models for BookstAI."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HITLStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"


@dataclass
class HITLStep:
    name: str
    content: Any
    status: HITLStatus = HITLStatus.PENDING
    edited_content: Any | None = None
    comment: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
