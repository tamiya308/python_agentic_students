from fastapi import APIRouter, HTTPException, Response, status
from pynamodb.exceptions import DeleteError, PutError

from src.db import StudentEnrolmentRecord as Record
from src.models.StudentEnrolments import StudentEnrolment, StudentEnrolmentUpdate

router = APIRouter(prefix="/StudentEnrolments", tags=["StudentEnrolments"])


def _to_model(record: Record) -> StudentEnrolment:
    return StudentEnrolment.model_validate(record.to_simple_dict())


def _to_record(enrolment: StudentEnrolment) -> Record:
    return Record(**enrolment.model_dump())


def _name_taken(name: str, exclude_id: int | None = None) -> bool:
    condition = Record.StudentName == name
    if exclude_id is not None:
        condition = condition & (Record.StudentId != exclude_id)
    return next(iter(Record.scan(filter_condition=condition)), None) is not None


def _is_conditional_failure(error: PutError | DeleteError) -> bool:
    return error.cause_response_code == "ConditionalCheckFailedException"


@router.get("", response_model=list[StudentEnrolment])
def getAllStudentEnrolments():
    return sorted((_to_model(r) for r in Record.scan()), key=lambda e: e.StudentId)


@router.get("/{id}", response_model=StudentEnrolment)
def getStudentEnrolments(id: int):
    try:
        return _to_model(Record.get(id))
    except Record.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "StudentEnrolment not found")


@router.post("", response_model=StudentEnrolment, status_code=status.HTTP_201_CREATED)
def postStudentEnrolments(body: StudentEnrolment):
    if _name_taken(body.StudentName):
        raise HTTPException(status.HTTP_409_CONFLICT, "StudentName already exists")
    try:
        _to_record(body).save(condition=Record.StudentId.does_not_exist())
    except PutError as error:
        if _is_conditional_failure(error):
            raise HTTPException(status.HTTP_409_CONFLICT, "StudentId already exists")
        raise
    return body


@router.put("/{id}", response_model=StudentEnrolment)
def putStudentEnrolments(id: int, body: StudentEnrolmentUpdate):
    if Record.count(id) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "StudentEnrolment not found")
    if _name_taken(body.StudentName, exclude_id=id):
        raise HTTPException(status.HTTP_409_CONFLICT, "StudentName already exists")
    enrolment = StudentEnrolment(StudentId=id, **body.model_dump())
    _to_record(enrolment).save()
    return enrolment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteStudentEnrolments(id: int):
    try:
        Record(StudentId=id).delete(condition=Record.StudentId.exists())
    except DeleteError as error:
        if _is_conditional_failure(error):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "StudentEnrolment not found")
        raise
    return Response(status_code=status.HTTP_204_NO_CONTENT)
