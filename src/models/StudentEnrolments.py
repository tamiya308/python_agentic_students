from pydantic import BaseModel, Field


class Unit(BaseModel):
    UnitId: int
    UnitName: str = Field(min_length=1)


class StudentEnrolmentUpdate(BaseModel):
    """Body for PUT: every field except StudentId and CourseName, which come from the path."""

    StudentName: str = Field(min_length=1)
    UnitsToComplete: list[Unit] = []


class StudentEnrolment(StudentEnrolmentUpdate):
    StudentId: int
    CourseName: str = Field(min_length=1)
