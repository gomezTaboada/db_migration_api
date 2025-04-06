import pytest
from fastapi import HTTPException
from app.utils.validate_payload_util import validate_payload_data
from app.utils.constants import MAX_RECORDS_TO_INSERT

def test_validate_payload_data_with_valid_data():
    payload = [{"field1": "value", "field2": 1} for _ in range(MAX_RECORDS_TO_INSERT)]
    
    # Should not raise exception
    assert validate_payload_data(payload) is None

def test_validate_payload_data_with_empty_list():
    payload = []

    with pytest.raises(HTTPException) as exc_info:
        validate_payload_data(payload)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid: No records to insert were found."

def test_validate_payload_data_with_too_many_records():
    payload = [{"field1": "value", "field2": 1} for _ in range(MAX_RECORDS_TO_INSERT + 1)]

    with pytest.raises(HTTPException) as exc_info:
        validate_payload_data(payload)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == f"Invalid: Max number of records allowed is {MAX_RECORDS_TO_INSERT}."