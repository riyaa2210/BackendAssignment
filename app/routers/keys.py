from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CreateAPIKeyRequest, APIKeyResponse
from app.services import key_service

router = APIRouter(prefix="/keys", tags=["API Keys"])


@router.post("/", response_model=APIKeyResponse)
def create_key(body: CreateAPIKeyRequest, db: Session = Depends(get_db)):
    key, raw_key = key_service.create_api_key(db, body.name)
    return {
        "id": key.id,
        "name": key.name,
        "raw_key": raw_key,
        "usage_count": key.usage_count,
        "created_at": key.created_at,
    }


@router.get("/")
def list_keys(db: Session = Depends(get_db)):
    keys = key_service.list_keys(db)
    # not returning key_hash obviously
    return [
        {
            "id": k.id,
            "name": k.name,
            "usage_count": k.usage_count,
            "is_active": k.is_active,
            "created_at": k.created_at,
        }
        for k in keys
    ]


@router.delete("/{key_id}")
def revoke_key(key_id: str, db: Session = Depends(get_db)):
    key = key_service.revoke_key(db, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="key not found")
    return {"message": "key revoked"}
