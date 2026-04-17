from fastapi import Request, HTTPException
from app.database import SessionLocal
from app.services.key_service import verify_key


# using this as a dependency in routes that need auth
async def require_api_key(request: Request):
    key_val = request.headers.get("X-API-Key")

    if not key_val:
        raise HTTPException(status_code=401, detail="no api key provided")

    db = SessionLocal()
    try:
        matched_key = verify_key(db, key_val)
        if matched_key is None:
            raise HTTPException(status_code=401, detail="key is invalid or has been revoked")

        request.state.api_key = matched_key
    finally:
        db.close()
