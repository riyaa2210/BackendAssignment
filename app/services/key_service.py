import uuid
import hashlib
from sqlalchemy.orm import Session
from app.models import APIKey


def make_hash(val: str) -> str:
    return hashlib.sha256(val.encode()).hexdigest()


def generate_key(db: Session, name: str):
    # strip dashes so it looks cleaner as an api key
    raw = str(uuid.uuid4()).replace("-", "")
    h = make_hash(raw)

    new_key = APIKey(
        label=name,
        hashed_key=h,
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    print(f"new key created for '{name}', starts with: {raw[:8]}")
    return new_key, raw


def verify_key(db: Session, raw: str):
    h = make_hash(raw)

    k = db.query(APIKey).filter(
        APIKey.hashed_key == h,
        APIKey.active == 1
    ).first()

    if k is None:
        return None

    k.hit_count += 1
    db.commit()
    return k


def get_all_keys(db: Session):
    return db.query(APIKey).all()


def disable_key(db: Session, kid: str):
    k = db.query(APIKey).filter(APIKey.id == kid).first()
    if not k:
        return None
    k.active = 0
    db.commit()
    return k
