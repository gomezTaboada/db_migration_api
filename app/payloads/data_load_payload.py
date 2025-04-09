from pydantic import BaseModel
from typing import List

from app.models import (
    Job, Department, Employee
)


class JobDataPayload(BaseModel):
    data: List[Job]

class DepartmentDataPayload(BaseModel):
    data: List[Department]

class EmployeeDataPayload(BaseModel):
    data: List[Employee]
