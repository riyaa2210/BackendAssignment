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
        print(f"incoming key: {key_val[:10]}...")  # debug - remove later
        matched_key = verify_key(db, key_val)
        if matched_key is None:
            raise HTTPException(status_code=401, detail="key is invalid or has been revoked")

        # store just the values we need, not the ORM object
        # if we store the object itself, session closes and we get DetachedInstanceError
        request.state.api_key_id = matched_key.id
        request.state.api_key_label = matched_key.label
    finally:
        db.close()
