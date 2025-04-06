MAX_RECORDS_TO_INSERT = 1

FILE_TABLE_DTYPE_MAPPING = {
    'job': {
        "id": "int64",
        "job": "string"
    },
    'department': {
        "id": "int64",
        "department": "string"
    },
    'employee' : {
        "id": "int64",
        "name": "string",
        "datetime": "string",
        "department_id": "int64",
        "job_id": "int64"
    }    
}