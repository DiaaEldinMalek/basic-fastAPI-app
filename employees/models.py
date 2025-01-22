from typing import Optional
from sqlmodel import Field, SQLModel


# model
class Employee(SQLModel, table=True):
    id: int = Field(primary_key=True, include=True)
    name: str = Field(index=True)
    age: int = Field(default=None, index=True, gt=0)
    department: str = Field(default=None)
    salary: float = Field(default=0)


class EmployeeUpdate(Employee):
    id: int | None = Field(default=None, exclude=True)
    name: Optional[str] = None
    age: Optional[int] = None
    department: Optional[str] = None
    salary: Optional[float] = None
