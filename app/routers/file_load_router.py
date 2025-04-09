from fastapi import APIRouter

from app.engine.database_session import SessionDep
from app.payloads.file_load_payload import FileLoadPayload
from app.service.load_from_file_service import load_data_from_files
from app.utils.database_insert_utils import bulk_insert_into_database

router = APIRouter(prefix="/file-load", tags=["file-load"])

@router.post("/", status_code=201)
async def upload_data_from_files(payload: FileLoadPayload, session: SessionDep) -> dict:
    valid_records, invalid_records = load_data_from_files(files=payload.files, table_name=payload.table_name)
    bulk_insert_into_database(data=valid_records, session=session)

    return {
        "message": f"Inserted records: {len(valid_records)}.",
        'invalid_records': invalid_records
    }
