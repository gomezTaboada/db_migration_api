from pydantic import BaseModel
from typing import List
from models.job import Job


class JobDataPayload(BaseModel):
    data: List[Job]
