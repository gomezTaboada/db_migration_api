import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.models import Job, Department, Employee
from app.engine.database_session import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="sample_departments")
def sample_departments_fixture(session: Session):
    departments = [
        Department(id=1, department="Engineering"),
        Department(id=2, department="Human Resources"),
    ]
    session.add_all(departments)
    session.commit()
    return departments

@pytest.fixture(name="sample_employees")
def sample_employees_fixture(session: Session, sample_departments, sample_jobs):
    employees = [
        Employee(id=1, name="Alice", datetime="2024-04-01T10:00:00", department_id=1, job_id=1),
        Employee(id=2, name="Bob", datetime="2024-04-01T11:00:00", department_id=2, job_id=2),
    ]
    session.add_all(employees)
    session.commit()
    return employees