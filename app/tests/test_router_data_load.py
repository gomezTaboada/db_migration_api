from fastapi.testclient import TestClient
from app.models.job import Job
from app.tests.fixtures import *


@pytest.fixture(name="sample_jobs")
def sample_jobs_fixture(session: Session):
    jobs = [
        Job(id=1, job="ETL Job"),
        Job(id=2, job="Data Sync"),
    ]
    session.add_all(jobs)
    session.commit()
    return jobs

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


def test_read_departments(client: TestClient, sample_departments: list[Department]):
    response = client.get("/data-load/department")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == len(sample_departments)
    assert data[0]["department"] == "Engineering"

def test_create_department(client: TestClient):
    new_departments = {
        'data': [{
            'id': 10,
            'department': 'Finance'
        }]
    }

    response = client.post("/data-load/department", json=new_departments)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data['message'] == f"Inserted records: {len(new_departments['data'])}."

def test_create_employee(client: TestClient, sample_departments, sample_jobs):
    new_employee = {
        'data': [{
            'id': 999,
            'name': 'Charlie',
            'datetime': '2024-04-02T12:00:00',
            'department_id': 1,
            'job_id': 1
        }]
    }

    response = client.post("/data-load/employee", json=new_employee)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data['message'] == f"Inserted records: {len(new_employee['data'])}."


def test_read_employees(client: TestClient, sample_employees: list[Employee]):
    response = client.get("/data-load/employee")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == len(sample_employees)
    assert data[0]["name"] == "Alice"
    assert "department_id" in data[0]
    assert "job_id" in data[0]    
    