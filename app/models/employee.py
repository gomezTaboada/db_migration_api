from sqlmodel import Field, SQLModel

class Employee(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field()
    datetime: str = Field()
    department_id: int = Field(foreign_key="department.id")
    job_id: int = Field(foreign_key="job.id")
