from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.db import get_table
from src.models.StudentEnrolments import StudentEnrolment, StudentEnrolmentUpdate

router = APIRouter(prefix="/StudentEnrolments", tags=["StudentEnrolments"])


def _scan_all(table, **kwargs) -> list[dict]:
    """Scan the whole table, following pagination."""
    items = []
    while True:
        page = table.scan(**kwargs)
        items.extend(page.get("Items", []))
        if "LastEvaluatedKey" not in page:
            return items
        kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]


def _name_taken(table, name: str, exclude_id: int | None = None) -> bool:
    condition = Attr("StudentName").eq(name)
    if exclude_id is not None:
        condition = condition & Attr("StudentId").ne(exclude_id)
    return bool(_scan_all(table, FilterExpression=condition))


def _is_conditional_failure(error: ClientError) -> bool:
    return error.response["Error"]["Code"] == "ConditionalCheckFailedException"


@router.get("", response_model=list[StudentEnrolment])
def getAllStudentEnrolments(table=Depends(get_table)):
    items = _scan_all(table)
    return sorted(
        (StudentEnrolment.model_validate(i) for i in items),
        key=lambda e: e.StudentId,
    )


@router.get("/{id}", response_model=StudentEnrolment)
def getStudentEnrolments(id: int, table=Depends(get_table)):
    item = table.get_item(Key={"StudentId": id}).get("Item")
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "StudentEnrolment not found")
    return StudentEnrolment.model_validate(item)


@router.post("", response_model=StudentEnrolment, status_code=status.HTTP_201_CREATED)
def postStudentEnrolments(body: StudentEnrolment, table=Depends(get_table)):
    if _name_taken(table, body.StudentName):
        raise HTTPException(status.HTTP_409_CONFLICT, "StudentName already exists")
    try:
        table.put_item(
            Item=body.model_dump(),
            ConditionExpression="attribute_not_exists(StudentId)",
        )
    except ClientError as error:
        if _is_conditional_failure(error):
            raise HTTPException(status.HTTP_409_CONFLICT, "StudentId already exists")
        raise
    return body


@router.put("/{id}", response_model=StudentEnrolment)
def putStudentEnrolments(
    id: int, body: StudentEnrolmentUpdate, table=Depends(get_table)
):
    if "Item" not in table.get_item(Key={"StudentId": id}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "StudentEnrolment not found")
    if _name_taken(table, body.StudentName, exclude_id=id):
        raise HTTPException(status.HTTP_409_CONFLICT, "StudentName already exists")
    record = StudentEnrolment(StudentId=id, **body.model_dump())
    table.put_item(Item=record.model_dump())
    return record


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteStudentEnrolments(id: int, table=Depends(get_table)):
    try:
        table.delete_item(
            Key={"StudentId": id},
            ConditionExpression="attribute_exists(StudentId)",
        )
    except ClientError as error:
        if _is_conditional_failure(error):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "StudentEnrolment not found")
        raise
    return Response(status_code=status.HTTP_204_NO_CONTENT)
