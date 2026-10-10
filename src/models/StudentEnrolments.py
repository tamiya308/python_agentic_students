from pydantic import BaseModel, Field


class Unit(BaseModel):
    UnitId: int
    UnitName: str = Field(min_length=1)


class StudentEnrolmentUpdate(BaseModel):
    """Body for PUT: every field except StudentId, which comes from the path."""

    StudentName: str = Field(min_length=1)
    CourseName: str | None = None
    UnitsToComplete: list[Unit] = []


class StudentEnrolment(StudentEnrolmentUpdate):
    StudentId: int
