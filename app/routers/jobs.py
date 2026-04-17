from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import JobRequest, JobStatusResponse
from app.services import job_service
from app.middleware import require_api_key
from app.rate_limiter import check_rate_limit

router = APIRouter(tags=["jobs"])


@router.post("/submit-job", response_model=JobStatusResponse)
async def submit_job(
    req: JobRequest,
    bg: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(require_api_key),
):
    curr_key = request.state.api_key

    # check rate limit before doing anything
    if check_rate_limit(curr_key.id):
        raise HTTPException(status_code=429, detail="too many requests, wait a bit")

    j = job_service.make_job(db, curr_key.id, req.payload)
    bg.add_task(job_service.process_job, j.id, req.payload)

    return j


@router.get("/job/{jid}", response_model=JobStatusResponse)
def get_job_status(jid: str, db: Session = Depends(get_db)):
    j = job_service.fetch_job(db, jid)
    if not j:
        raise HTTPException(status_code=404, detail="no job with that id")
    return j
