from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewKeyRequest(BaseModel):
    name: str


# this is what we send back after creating a key
# raw_key only shown once so user better save it lol
class KeyCreatedResponse(BaseModel):
    id: str
    name: str
    raw_key: str
    hit_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class JobRequest(BaseModel):
    payload: Optional[str] = "some task"


class JobStatusResponse(BaseModel):
    id: str
    status: str
    result: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
