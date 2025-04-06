from fastapi import APIRouter, Query
from typing import Annotated
from sqlmodel import select

from engine.database_engine import (
    SessionDep
)
from models.job import Job
from payloads.data_load_payload import JobDataPayload
from utils.validate_payload_util import validate_payload_data


router = APIRouter(prefix="/data-load", tags=["data-load"])

@router.post("/job")
async def create_job(payload: JobDataPayload, session: SessionDep) -> dict:
    validate_payload_data(payload_data=payload.data)
    session.add_all(instances=payload.data)
    session.commit()

    return {"message": f"Inserted {len(payload.data)} records."}

@router.get("/job")
async def read_jobs(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs
