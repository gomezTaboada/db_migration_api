import os
from sqlmodel import SQLModel, create_engine

from app.utils.credentials_utils import load_credentials_as_json


if not os.getenv("ENVIRONMENT") or os.getenv("ENVIRONMENT") != 'CLOUD':
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
else:
    credentials = load_credentials_as_json(environment_variable_name='DATABASE_CREDENTIALS')
    db_user = credentials['user']
    db_pass = credentials["password"]
    db_name = credentials["name"]
    db_host = credentials["host"]

    # PostgreSQL connection string using Unix socket
    postgres_url = (
        f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}"
        f"?host={db_host}"
    )

    engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)
