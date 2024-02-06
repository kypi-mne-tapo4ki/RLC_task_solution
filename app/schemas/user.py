from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegistrationResponse(BaseModel):
    token: str


class UserCheckResponse(BaseModel):
    username: str
    created_at: datetime
    updated_at: Optional[datetime]
    token_expiry: datetime
