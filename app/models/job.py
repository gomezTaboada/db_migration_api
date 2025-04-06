from sqlmodel import Field, SQLModel


class Job(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    job: str = Field()
