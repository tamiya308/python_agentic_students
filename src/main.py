from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import load_env

load_env()

from src.api import StudentEnrolments  # noqa: E402
from src.db import configure_db, create_table_if_missing  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_db()
    create_table_if_missing()
    yield


app = FastAPI(title="Student Enrolments API", lifespan=lifespan)
app.include_router(StudentEnrolments.router)
