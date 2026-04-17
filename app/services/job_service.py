import time
import uuid
from sqlalchemy.orm import Session
from app.models import Job
from app.database import SessionLocal
from sqlalchemy.sql import func


def make_job(db: Session, key_id: str, payload: str):
    j = Job(
        id=str(uuid.uuid4()),
        status="pending",
        owner_key_id=key_id,
    )
    db.add(j)
    db.commit()
    db.refresh(j)
    print(f"job queued: {j.id[:8]}")
    return j


def process_job(job_id: str, payload: str):
    # need a fresh db session here, the request one is already closed
    db = SessionLocal()

    try:
        j = db.query(Job).filter(Job.id == job_id).first()
        if j is None:
            print(f"couldnt find job {job_id}, skipping")
            return

        j.status = "running"
        db.commit()

        print(f"working on job {job_id[:8]}...")
        time.sleep(3)  # pretend we're doing something heavy

        j.status = "done"
        j.result = f"finished processing: {payload}"
        j.finished_at = func.now()
        db.commit()

        print(f"job {job_id[:8]} done")

    except Exception as err:
        print(f"job {job_id[:8]} crashed: {err}")
        # re-fetch because the obj might be in a bad state after exception
        try:
            j2 = db.query(Job).filter(Job.id == job_id).first()
            if j2:
                j2.status = "failed"
                j2.result = f"error: {str(err)}"
                db.commit()
        except:
            print("couldnt even update the failed status, something is really wrong")
    finally:
        db.close()


def fetch_job(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()
