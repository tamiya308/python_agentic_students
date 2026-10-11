from fastapi import APIRouter, HTTPException, Response, status
from pynamodb.exceptions import DeleteError, PutError

from src.db import StudentEnrolmentRecord as Record
from src.models.StudentEnrolments import StudentEnrolment, StudentEnrolmentUpdate

router = APIRouter(prefix="/StudentEnrolments", tags=["StudentEnrolments"])

NOT_FOUND = "StudentEnrolment not found"


def _to_model(record: Record) -> StudentEnrolment:
    return StudentEnrolment.model_validate(record.to_simple_dict())


def _to_record(enrolment: StudentEnrolment) -> Record:
    return Record(**enrolment.model_dump())


def _check_student_name(id: int, name: str, course: str | None = None):
    """Raise 409 unless `name` is free for student `id`.

    A name belongs to one StudentId, and every course item for that student
    carries the same name. `course` is the item being replaced, so its old name
    doesn't count as a mismatch.
    """
    used_by_other = Record.scan(
        filter_condition=(Record.StudentName == name) & (Record.StudentId != id)
    )
    if next(iter(used_by_other), None) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "StudentName already exists")
    if any(r.StudentName != name for r in Record.query(id) if r.CourseName != course):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "StudentName does not match the student's other enrolments",
        )


def _is_conditional_failure(error: PutError | DeleteError) -> bool:
    return error.cause_response_code == "ConditionalCheckFailedException"


@router.get("", response_model=list[StudentEnrolment])
def getAllStudentEnrolments():
    return sorted(
        (_to_model(r) for r in Record.scan()),
        key=lambda e: (e.StudentId, e.CourseName),
    )


@router.get("/{id}", response_model=list[StudentEnrolment])
def getStudentEnrolments(id: int):
    enrolments = [_to_model(r) for r in Record.query(id)]
    if not enrolments:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
    return enrolments


@router.get("/{id}/{courseName}", response_model=StudentEnrolment)
def getStudentCourseEnrolment(id: int, courseName: str):
    try:
        return _to_model(Record.get(id, courseName))
    except Record.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)


@router.post("", response_model=StudentEnrolment, status_code=status.HTTP_201_CREATED)
def postStudentEnrolments(body: StudentEnrolment):
    _check_student_name(body.StudentId, body.StudentName)
    try:
        _to_record(body).save(condition=Record.StudentId.does_not_exist())
    except PutError as error:
        if _is_conditional_failure(error):
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Student is already enrolled in this course"
            )
        raise
    return body


@router.put("/{id}/{courseName}", response_model=StudentEnrolment)
def putStudentEnrolments(id: int, courseName: str, body: StudentEnrolmentUpdate):
    if Record.count(id, Record.CourseName == courseName) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
    _check_student_name(id, body.StudentName, course=courseName)
    enrolment = StudentEnrolment(
        StudentId=id, CourseName=courseName, **body.model_dump()
    )
    _to_record(enrolment).save()
    return enrolment


@router.delete("/{id}/{courseName}", status_code=status.HTTP_204_NO_CONTENT)
def deleteStudentEnrolments(id: int, courseName: str):
    try:
        Record(StudentId=id, CourseName=courseName).delete(
            condition=Record.StudentId.exists()
        )
    except DeleteError as error:
        if _is_conditional_failure(error):
            raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
        raise
    return Response(status_code=status.HTTP_204_NO_CONTENT)
