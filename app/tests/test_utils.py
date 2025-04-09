import pytest
from fastapi import HTTPException
from app.utils.validate_payload_util import validate_records, validate_payload_data
from app.models import Job, Department, Employee
from app.utils.constants import MAX_RECORDS_TO_INSERT

def test_validate_records_all_valid():
    payload = [
        {"id": 1, "job": "ETL"},
        {"id": 2, "job": "Data Sync"}
    ]

    valid, invalid = validate_records(Job, payload)

    assert len(valid) == 2
    assert len(invalid) == 0
    assert valid[0].job == "ETL"


def test_validate_records_some_invalid():
    payload = [
        {"id": 1, "job": "Analyst"},
        {"id": 2},  # Missing 'job'
        {"job": "Engineer"}  # Missing 'id'
    ]

    valid, invalid = validate_records(Job, payload)

    assert len(valid) == 1
    assert len(invalid) == 2
    assert invalid[0]["index"] == 1
    assert "errors" in invalid[0]
    assert invalid[0]["errors"][0]["loc"] == ("job",)  # Missing required field


def test_validate_records_all_invalid():
    payload = [
        {"invalid_field": "oops"},
        {}
    ]

    valid, invalid = validate_records(Department, payload)

    assert len(valid) == 0
    assert len(invalid) == 2



def test_validate_payload_data_all_valid():
    payload = [
        {"id": 1, "department": "HR"}
    ]

    valid, invalid = validate_payload_data(Department, payload)

    assert len(valid) == 1
    assert len(invalid) == 0
    assert valid[0].department == "HR"


def test_validate_payload_data_empty_payload():
    with pytest.raises(HTTPException) as exc:
        validate_payload_data(Department, [])

    assert exc.value.status_code == 400
    assert "No records to insert" in exc.value.detail


def test_validate_payload_data_too_many_records():
    payload = [{"id": i, "department": f"Dept {i}"} for i in range(MAX_RECORDS_TO_INSERT + 1)]

    with pytest.raises(HTTPException) as exc:
        validate_payload_data(Department, payload)

    assert exc.value.status_code == 400
    assert "Max number of records" in exc.value.detail


def test_validate_payload_data_with_invalid_records():
    payload = [
        {"name": "Bob"},  # missing required fields
    ]

    valid, invalid = validate_payload_data(Employee, payload)

    assert len(valid) == 0
    assert len(invalid) == 1
    assert "errors" in invalid[0]
