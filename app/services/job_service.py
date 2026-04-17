import time
import uuid
from sqlalchemy.orm import Session
from app.models import Job
from app.database import SessionLocal


def create_job(db: Session, api_key_id: str, payload: str) -> Job:
    job = Job(
        id=str(uuid.uuid4()),
        status="pending",
        api_key_id=api_key_id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    print(f"[job_service] job {job.id[:8]} created")
    return job


def run_job(job_id: str, payload: str):
    # background task — gets its own db session since FastAPI closes the request one
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            print(f"[job_service] job {job_id} not found, skipping")
            return

        job.status = "running"
        db.commit()

        # simulate doing actual work
        print(f"[job_service] processing job {job_id[:8]}...")
        time.sleep(3)

        job.status = "done"
        job.result = f"processed: {payload}"
        db.commit()
        print(f"[job_service] job {job_id[:8]} finished")

    except Exception as e:
        print(f"[job_service] job {job_id[:8]} failed: {e}")
        # re-query because the job object might be detached after the exception
        try:
            failed_job = db.query(Job).filter(Job.id == job_id).first()
            if failed_job:
                failed_job.status = "failed"
                failed_job.result = str(e)
                db.commit()
        except Exception as inner:
            print(f"[job_service] couldn't update failed status: {inner}")
    finally:
        db.close()


def get_job(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()
