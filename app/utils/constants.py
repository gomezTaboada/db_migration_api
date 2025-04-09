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

AVRO_SCHEMA_MAPPING = {
    'job': {
        "name": "Job",
        "type": "record",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "job", "type": "string"}
        ]
    },
    'department': {
        "name": "Department",
        "type": "record",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "department", "type": "string"}
        ]
    },
    'employee': {
        "name": "Employee",
        "type": "record",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "string"},
            {"name": "datetime", "type": "string"},
            {"name": "department_id", "type": "int"},
            {"name": "job_id", "type": "int"}
        ]
    }
}