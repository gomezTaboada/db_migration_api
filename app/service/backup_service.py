import os
from io import BytesIO
from google.cloud import storage
from sqlmodel import select, SQLModel, delete
from fastavro import parse_schema, writer, reader
from sqlalchemy import text

from app.engine.database_session import SessionDep
from app.utils.class_utils import get_table_class
from app.utils.constants import AVRO_SCHEMA_MAPPING


def create_avro_file_bytes_buffer(session: SessionDep, table_name: str) -> bytes:

    table_class = get_table_class(table_name=table_name)

    records: list[SQLModel] = session.exec(select(table_class)).all()
    records_data = [record.model_dump() for record in records]

    print(records_data)

    avro_schema = AVRO_SCHEMA_MAPPING[table_name]
    parsed_schema = parse_schema(schema=avro_schema)

    buffer = BytesIO()
    writer(fo=buffer, schema=parsed_schema, records=records_data)
    buffer.seek(0)

    return buffer


def upload_bytes_to_cloud_storage(buffer_data: bytes, bucket_name: str, relative_file_path: str) -> None:
    client = storage.Client(project=os.getenv('STORAGE_PROJECT_ID'))
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=relative_file_path)
    
    blob.upload_from_file(file_obj=buffer_data, rewind=True, content_type="application/octet-stream")

    return


def read_avro_from_gcs(bucket_name: str, relative_file_path: str) -> list:
    client = storage.Client(project=os.getenv('STORAGE_PROJECT_ID'))
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=relative_file_path)
    
    buffer = BytesIO()
    blob.download_to_file(file_obj=buffer)
    buffer.seek(0)

    avro_reader = reader(buffer)
    records = [record for record in avro_reader]

    return records

def restore_table_from_records(session: SessionDep, table_name: str, data: list[dict]) -> None:
    table_class = get_table_class(table_name=table_name)
    session.exec(delete(table_class))

    objects = [table_class(**row) for row in data]
    session.add_all(instances=objects)
    session.commit()

    return