from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./myapp.db")

# sqlite needs this flag otherwise it throws threading errors
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
