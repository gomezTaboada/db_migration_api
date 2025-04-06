import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.models.job import Job
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
