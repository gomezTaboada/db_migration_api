from fastapi import APIRouter

from app.engine.database_session import SessionDep
from app.payloads.backup_payload import BackupPayload, RestoreBackupPayload
from app.service.backup_service import (
    create_avro_file_bytes_buffer,
    upload_bytes_to_cloud_storage,
    read_avro_from_gcs,
    restore_table_from_records
)

router = APIRouter(prefix="/backup", tags=["backup"])

@router.post("/", status_code=201)
async def backup_table_into_avro_file(payload: BackupPayload, session: SessionDep) -> dict:
    buffer_data = create_avro_file_bytes_buffer(session=session, table_name=payload.table_name)
    upload_bytes_to_cloud_storage(
        buffer_data=buffer_data, bucket_name=payload.bucket_name, relative_file_path=payload.relative_file_path
    )
    
    return {
        "message": f"Uploaded Avro file to gs://{payload.bucket_name}/{payload.relative_file_path}"
    }


@router.post("/restore/", status_code=201)
async def restore_table_from_backup_file(payload: RestoreBackupPayload, session: SessionDep) -> dict:
    records_data = read_avro_from_gcs(bucket_name=payload.bucket_name, relative_file_path=payload.relative_file_path)
    restore_table_from_records(session=session, table_name=payload.table_name, data=records_data)

    return {
        "message": f"Table {payload.table_name} was restored from gs://{payload.bucket_name}/{payload.relative_file_path}"
    }
