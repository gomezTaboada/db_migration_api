from pydantic import BaseModel

class BackupPayload(BaseModel):
    table_name: str
    bucket_name: str
    relative_file_path: str

class RestoreBackupPayload(BaseModel):
    table_name: str
    bucket_name: str
    relative_file_path: str
