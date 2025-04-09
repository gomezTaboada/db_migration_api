from app.engine.database_session import (
    SessionDep
)

def bulk_insert_into_database(data: list, session: SessionDep) -> None:
    session.add_all(instances=data)
    session.commit()

    return