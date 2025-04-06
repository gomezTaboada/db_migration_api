from pydantic import BaseModel
from typing import List
from app.models.job import Job


class JobDataPayload(BaseModel):
    data: List[Job]
