from fastapi import APIRouter, Query
from typing import Annotated
from sqlmodel import select

from engine.database_engine import (
    SessionDep
)
from models.job import Job


router = APIRouter(prefix="/data-load", tags=["data-load"])

@router.post("/job", tags=["job"])
async def create_job(job: Job, session: SessionDep) -> Job:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

@router.get("/job", tags=["job"])
async def read_jobs(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs
