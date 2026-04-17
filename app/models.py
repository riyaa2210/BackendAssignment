from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    key_hash = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Integer, default=1)  # 1 active, 0 revoked


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="pending")  # pending, running, done, failed
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    api_key_id = Column(String, nullable=True)
