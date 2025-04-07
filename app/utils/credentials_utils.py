import os
import json


def load_credentials_as_json(environment_variable_name: str) -> dict:
    raw_credentials = os.getenv(environment_variable_name)

    credentials = json.loads(raw_credentials)
    return credentials