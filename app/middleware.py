from fastapi import Request, HTTPException
from app.database import SessionLocal
from app.services.key_service import validate_api_key


async def require_api_key(request: Request):
    raw_key = request.headers.get("X-API-Key")
    if not raw_key:
        raise HTTPException(status_code=401, detail="missing api key")

    db = SessionLocal()
    try:
        key = validate_api_key(db, raw_key)
        if not key:
            raise HTTPException(status_code=401, detail="invalid or revoked api key")
        # attach to request state so routes can use it
        request.state.api_key = key
    finally:
        db.close()
