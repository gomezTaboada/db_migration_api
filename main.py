from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
import uvicorn
from typing import Annotated
from sqlmodel import select

from engine.database_engine import (
    create_db_and_tables,
    SessionDep
)
from models.job import Job

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/job/")
def create_job(job: Job, session: SessionDep) -> Job:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

@app.get("/job/")
def read_jobs(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs

if __name__ == '__main__':
    uvicorn.run(app=app)
