from pydantic import BaseModel
from typing import List

class FileLoadPayload(BaseModel):
    files: List[str]
    table_name: str

