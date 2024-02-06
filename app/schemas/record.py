from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecordBase(BaseModel):
    """Base Record model."""

    title: str
    content: str
    tag: str


class RecordPayload(RecordBase):
    """Record payload model."""


class RecordResponse(RecordBase):
    """Record response model."""

    id: int
    created_by: int
    created_at: datetime


class RecordUpdatePayload(RecordBase):
    """Record update payload."""

    title: Optional[str] = None
    content: Optional[str] = None
    tag: Optional[str] = None
