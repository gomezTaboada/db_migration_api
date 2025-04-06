from fastapi import HTTPException
from utils.constants import MAX_RECORDS_TO_INSERT

def validate_payload_data(payload_data: list, max_records: int = MAX_RECORDS_TO_INSERT) -> None:
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

    return