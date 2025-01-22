from typing import Optional
from fastapi import HTTPException
from fastapi.routing import APIRouter
from sqlmodel import select, and_

from employees.models import Employee, EmployeeUpdate
from database import SessionDep
import utils


employee_router = APIRouter(prefix="/employees", tags=["employee"])


def get_employee_by_id(session: SessionDep, employee_id: int | str):
    """Helper method to retrieve Employee from DB"""
    try:
        empl = session.get(Employee, employee_id)
        return empl
    except OverflowError:
        raise HTTPException(400, "Invalid employee ID")


@employee_router.post("")
async def add_employee(
    session: SessionDep,
    employee: Employee,
) -> Employee:
    employee.id = utils.generate_random_id()
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


@employee_router.get("")
async def get_employees(
    session: SessionDep,
    name: Optional[str] = None,
    department: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    offset: int = 0,
    limit: int = 5,
) -> list[Employee]:
    conditions = {
        name: Employee.name == name,
        department: Employee.department == department,
        min_age: Employee.age.__ge__(min_age) if min_age is not None else True,
        max_age: Employee.age.__le__(max_age) if max_age is not None else True,
        min_salary: (
            Employee.salary.__ge__(min_salary) if min_salary is not None else True
        ),
        max_salary: (
            Employee.salary.__le__(max_salary) if max_salary is not None else True
        ),
    }

    applied_conditions = []

    for value, condition in conditions.items():
        if value is not None:
            applied_conditions.append(condition)

    employees = session.exec(
        select(Employee)
        .where(and_(True, *applied_conditions))
        .offset(offset)
        .limit(limit)
    ).all()
    return employees


@employee_router.put("/{employee_id}")
async def update_employee(
    session: SessionDep, employee_id: int, updated_data: EmployeeUpdate
):

    employee_data = get_employee_by_id(session, employee_id)

    if not employee_data:
        raise HTTPException(404, "Employee not found")
    new_data = updated_data.model_dump(exclude_unset=True)

    employee_data.sqlmodel_update(new_data)
    session.add(employee_data)
    session.commit()
    session.refresh(employee_data)

    return employee_data


@employee_router.delete("/{employee_id}")
async def remove_employee(session: SessionDep, employee_id: int):
    empl = get_employee_by_id(session, employee_id)
    if not empl:
        raise HTTPException(404, "Employee not found")

    session.delete(empl)
    session.commit()
    return "OK"
