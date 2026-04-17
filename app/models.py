from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    hashed_key = Column(String, unique=True, nullable=False)
    label = Column(String, nullable=False)   # just a name so we know whose key it is
    hit_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    active = Column(Integer, default=1)  # 0 means revoked


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="pending")
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    finished_at = Column(DateTime, nullable=True)
    owner_key_id = Column(String, nullable=True)  # which api key submitted this
