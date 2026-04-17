from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SubmitJobRequest, JobResponse
from app.services import job_service
from app.middleware import require_api_key
from app.rate_limiter import is_rate_limited

router = APIRouter(tags=["Jobs"])


@router.post("/submit-job", response_model=JobResponse)
async def submit_job(
    body: SubmitJobRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(require_api_key),
):
    api_key = request.state.api_key

    if is_rate_limited(api_key.id):
        raise HTTPException(status_code=429, detail="rate limit exceeded, slow down")

    job = job_service.create_job(db, api_key.id, body.payload)
    background_tasks.add_task(job_service.run_job, job.id, body.payload)
    return job


@router.get("/job/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = job_service.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job
