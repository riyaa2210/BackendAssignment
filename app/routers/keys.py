from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import NewKeyRequest, KeyCreatedResponse
from app.services import key_service

router = APIRouter(prefix="/keys", tags=["keys"])


@router.post("/", response_model=KeyCreatedResponse)
def create_key(body: NewKeyRequest, db: Session = Depends(get_db)):
    k, raw = key_service.generate_key(db, body.name)

    # manually building response so we can include raw key
    return {
        "id": k.id,
        "name": k.label,
        "raw_key": raw,
        "hit_count": k.hit_count,
        "created_at": k.created_at,
    }


@router.get("/")
def list_all_keys(db: Session = Depends(get_db)):
    all_keys = key_service.get_all_keys(db)
    result = []
    for k in all_keys:
        result.append({
            "id": k.id,
            "name": k.label,
            "hit_count": k.hit_count,
            "active": k.active,
            "created_at": k.created_at,
        })
    return result


@router.delete("/{kid}")
def revoke_key(kid: str, db: Session = Depends(get_db)):
    k = key_service.disable_key(db, kid)
    if k is None:
        raise HTTPException(status_code=404, detail="key not found")
    return {"msg": "key disabled"}
