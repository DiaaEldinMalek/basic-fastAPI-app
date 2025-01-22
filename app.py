import contextlib
from fastapi import FastAPI
from database import create_db_and_tables

from employees.controllers import employee_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # seed the database
    yield
    print("Shutting down application")


app = FastAPI(lifespan=lifespan)


app.include_router(employee_router)
