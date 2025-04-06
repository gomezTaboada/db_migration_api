from fastapi.testclient import TestClient
from app.models.job import Job
from app.tests.fixtures import *


def test_read_jobs(client: TestClient, sample_jobs: list[Job]):
    response = client.get("/data-load/job")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == len(sample_jobs)
    assert data[0]["job"] == "ETL Job"


def test_create_job(client: TestClient):

    new_job = {
        'data': [{
            'id': 123,
            'job': 'Data Analyst'
        }]
    }

    response = client.post("/data-load/job", json=new_job)

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data, dict)
    assert data['message'] == f"Inserted records: {len(new_job['data'])}."