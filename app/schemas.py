from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateAPIKeyRequest(BaseModel):
    name: str


class APIKeyResponse(BaseModel):
    id: str
    name: str
    raw_key: str  # only returned once at creation
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class SubmitJobRequest(BaseModel):
    payload: Optional[str] = "default task"


class JobResponse(BaseModel):
    id: str
    status: str
    result: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
