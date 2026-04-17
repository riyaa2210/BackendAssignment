import uuid
import hashlib
from sqlalchemy.orm import Session
from app.models import APIKey


def hash_key(raw_key: str) -> str:
    # sha256 is good enough here, not storing passwords so bcrypt is overkill
    return hashlib.sha256(raw_key.encode()).hexdigest()


def create_api_key(db: Session, name: str):
    raw_key = str(uuid.uuid4()).replace("-", "")  # cleaner looking key
    hashed = hash_key(raw_key)

    key = APIKey(
        name=name,
        key_hash=hashed,
    )
    db.add(key)
    db.commit()
    db.refresh(key)

    print(f"[key_service] created new key for '{name}' -> {raw_key[:8]}...")
    return key, raw_key


def validate_api_key(db: Session, raw_key: str):
    hashed = hash_key(raw_key)
    key = db.query(APIKey).filter(
        APIKey.key_hash == hashed,
        APIKey.is_active == 1
    ).first()

    if not key:
        return None

    # bump usage count
    key.usage_count += 1
    db.commit()
    return key


def list_keys(db: Session):
    return db.query(APIKey).all()


def revoke_key(db: Session, key_id: str):
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not key:
        return None
    key.is_active = 0
    db.commit()
    return key
