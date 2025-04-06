from sqlmodel import Field, SQLModel, Relationship

class Job(SQLModel, table=True):
    id: int = Field(primary_key=True)
    job: str = Field()
