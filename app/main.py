from fastapi import FastAPI
from app.database import engine, Base
from app.routers import keys, jobs

# create tables on startup — fine for dev, would use alembic in prod
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Key Manager",
    description="Simple API key management with rate limiting and background jobs",
    version="1.0.0"
)

app.include_router(keys.router)
app.include_router(jobs.router)


@app.get("/")
def root():
    return {"message": "server is running"}
