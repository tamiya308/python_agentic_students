from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from src.api import StudentEnrolments  # noqa: E402
from src.db import create_table_if_missing, get_dynamodb_resource  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table_if_missing(get_dynamodb_resource())
    yield


app = FastAPI(title="Student Enrolments API", lifespan=lifespan)
app.include_router(StudentEnrolments.router)
