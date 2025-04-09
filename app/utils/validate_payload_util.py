from fastapi import HTTPException
from app.utils.constants import MAX_RECORDS_TO_INSERT
from typing import Type, Tuple
from pydantic import ValidationError
from sqlmodel import SQLModel

def validate_records(model: Type[SQLModel], payload_data: list[dict]) -> Tuple[list[SQLModel], list[dict]]:
    valid_records = []
    invalid_records = []

    for index, item in enumerate(payload_data):
        try:
            obj = model.model_validate(item)
            valid_records.append(obj)

        except ValidationError as e:
            invalid_records.append({
                "index": index,
                "data": item,
                "errors": e.errors()
            })

    return valid_records, invalid_records

def validate_payload_data(model: SQLModel, payload_data: list, max_records: int = MAX_RECORDS_TO_INSERT) -> Tuple[list[SQLModel], list[dict]]:
    number_of_records = len(payload_data)

    if number_of_records == 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid: No records to insert were found."
        )

    if number_of_records > max_records:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid: Max number of records allowed is {max_records}."
        )

    valid_records, invalid_records = validate_records(model=model, payload_data=payload_data)

    return valid_records, invalid_records