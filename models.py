from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(index=True)
    password: str
