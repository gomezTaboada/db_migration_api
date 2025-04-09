from fastapi import HTTPException
from sqlmodel import SQLModel

from app.models import Job, Department, Employee

def get_table_class(table_name: str) -> SQLModel:
    if table_name == 'job':
        return Job
    elif table_name == 'department':
        return Department
    elif table_name == 'employee':
        return Employee
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid table_name field value: {table_name}."
        )
