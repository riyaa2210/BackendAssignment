from fastapi import FastAPI
from app.database import engine, Base
from app.routers import keys, jobs

# auto create tables, not using alembic for now
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Key Manager", version="1.0.0")

app.include_router(keys.router)
app.include_router(jobs.router)


@app.get("/")
def index():
    return {"status": "ok"}
