from sqlmodel import Field, SQLModel


class Department(SQLModel, table=True):
    id: int = Field(primary_key=True)
    department: str = Field()
