from fastapi import APIRouter, Query
from typing import Annotated
from sqlmodel import select

from app.engine.database_session import (
    SessionDep
)
from app.models import (
    Job, Department, Employee
)
from app.payloads.data_load_payload import (
    JobDataPayload,
    DepartmentDataPayload,
    EmployeeDataPayload
)
from app.utils.validate_payload_util import validate_payload_data
from app.utils.database_insert_utils import bulk_insert_into_database


router = APIRouter(prefix="/data-load", tags=["data-load"])

@router.post("/job", status_code=201)
async def create_job(payload: JobDataPayload, session: SessionDep) -> dict:
    validate_payload_data(payload_data=payload.data)
    bulk_insert_into_database(data=payload.data, session=session)

    return {"message": f"Inserted records: {len(payload.data)}."}

@router.get("/job")
async def read_jobs(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs


@router.post("/department", status_code=201)
async def create_department(payload: DepartmentDataPayload, session: SessionDep) -> dict:
    validate_payload_data(payload_data=payload.data)
    bulk_insert_into_database(data=payload.data, session=session)

    return {"message": f"Inserted records: {len(payload.data)}."}

@router.get("/department")
async def read_departments(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Department]:
    departments = session.exec(select(Department).offset(offset).limit(limit)).all()
    return departments


@router.post("/employee", status_code=201)
async def create_employee(payload: EmployeeDataPayload, session: SessionDep) -> dict:
    validate_payload_data(payload_data=payload.data)
    bulk_insert_into_database(data=payload.data, session=session)

    return {"message": f"Inserted records: {len(payload.data)}."}

@router.get("/employee")
async def read_employees(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Employee]:
    employees = session.exec(select(Employee).offset(offset).limit(limit)).all()
    return employees
