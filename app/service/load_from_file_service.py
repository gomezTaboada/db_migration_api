from typing import List
import pandas as pd

from app.utils.constants import FILE_TABLE_DTYPE_MAPPING
from app.utils.validate_payload_util import validate_records
from app.utils.class_utils import get_table_class


def load_data_from_files(files: List[str], table_name: str) -> dict:
    dtype = FILE_TABLE_DTYPE_MAPPING[table_name]
    headers = list(dtype.keys())

    df_files = []
    for file_path in files:
        df_file = pd.read_csv(filepath_or_buffer=file_path, sep=",", encoding='utf-8', dtype=dtype, names=headers)
        df_files.append(df_file)


    df_upload = pd.concat(df_files, ignore_index=True)

    upload_records = df_upload.to_dict(orient='records')

    table_class = get_table_class(table_name=table_name)
    valid_records, invalid_records = validate_records(model=table_class, payload_data=upload_records)

    return valid_records, invalid_records
