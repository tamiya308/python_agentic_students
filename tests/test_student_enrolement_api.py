import pytest
from fastapi.testclient import TestClient

from src.db import StudentEnrolmentRecord as Record
from src.main import app

ALAN = {
    "StudentId": 1000,
    "StudentName": "Alan Jones",
    "CourseName": "Commerce",
    "UnitsToComplete": [
        {"UnitId": 20, "UnitName": "Introduction to business"},
        {"UnitId": 21, "UnitName": "Managements basics"},
    ],
}
ALAN_LAW = {
    "StudentId": 1000,
    "StudentName": "Alan Jones",
    "CourseName": "Law",
    "UnitsToComplete": [{"UnitId": 60, "UnitName": "Contract law"}],
}
MEI = {
    "StudentId": 1003,
    "StudentName": "Mei Chen",
    "CourseName": "Nursing",
    "UnitsToComplete": [{"UnitId": 50, "UnitName": "Anatomy and physiology"}],
}


def add(item: dict):
    Record(**item).save()


@pytest.fixture
def client(db):
    # No `with` block, so the startup lifespan (real DynamoDB) doesn't run.
    return TestClient(app)


# GET /StudentEnrolments


def test_get_all_returns_200_ordered_by_student_id_then_course(client):
    add(MEI)
    add(ALAN_LAW)
    add(ALAN)
    response = client.get("/StudentEnrolments")
    assert response.status_code == 200
    assert [(e["StudentId"], e["CourseName"]) for e in response.json()] == [
        (1000, "Commerce"),
        (1000, "Law"),
        (1003, "Nursing"),
    ]


def test_get_all_returns_200_empty_list(client):
    response = client.get("/StudentEnrolments")
    assert response.status_code == 200
    assert response.json() == []


# GET /StudentEnrolments/{id}


def test_get_student_returns_200_with_every_course(client):
    add(ALAN)
    add(ALAN_LAW)
    add(MEI)
    response = client.get("/StudentEnrolments/1000")
    assert response.status_code == 200
    assert response.json() == [ALAN, ALAN_LAW]


def test_get_student_returns_404_when_missing(client):
    assert client.get("/StudentEnrolments/9999").status_code == 404


# GET /StudentEnrolments/{id}/{courseName}


def test_get_course_returns_200(client):
    add(ALAN)
    add(ALAN_LAW)
    response = client.get("/StudentEnrolments/1000/Law")
    assert response.status_code == 200
    assert response.json() == ALAN_LAW


def test_get_course_returns_404_when_missing(client):
    add(ALAN)
    assert client.get("/StudentEnrolments/1000/Law").status_code == 404


# POST /StudentEnrolments


def test_post_returns_201_with_created_record(client):
    response = client.post("/StudentEnrolments", json=ALAN)
    assert response.status_code == 201
    assert response.json() == ALAN
    assert Record.get(1000, "Commerce").StudentName == "Alan Jones"


def test_post_adds_another_course_for_existing_student(client):
    add(ALAN)
    response = client.post("/StudentEnrolments", json=ALAN_LAW)
    assert response.status_code == 201
    assert Record.count(1000) == 2


def test_post_returns_409_on_duplicate_student_and_course(client):
    add(ALAN)
    response = client.post("/StudentEnrolments", json=ALAN)
    assert response.status_code == 409


def test_post_returns_409_on_student_name_used_by_another_student(client):
    add(ALAN)
    response = client.post("/StudentEnrolments", json={**ALAN, "StudentId": 2000})
    assert response.status_code == 409


def test_post_returns_409_on_name_mismatch_with_other_courses(client):
    add(ALAN)
    response = client.post(
        "/StudentEnrolments", json={**ALAN_LAW, "StudentName": "Someone Else"}
    )
    assert response.status_code == 409


@pytest.mark.parametrize(
    "body",
    [
        {k: v for k, v in ALAN.items() if k != "StudentName"},
        {k: v for k, v in ALAN.items() if k != "CourseName"},
        {**ALAN, "CourseName": ""},
        {**ALAN, "StudentId": "not-a-number"},
        {**ALAN, "UnitsToComplete": [{"UnitId": 20}]},
    ],
)
def test_post_returns_422_on_invalid_input(client, body):
    assert client.post("/StudentEnrolments", json=body).status_code == 422


# PUT /StudentEnrolments/{id}/{courseName}


def test_put_returns_200_and_replaces_whole_record(client):
    add(ALAN)
    response = client.put(
        "/StudentEnrolments/1000/Commerce", json={"StudentName": "Al Jones"}
    )
    assert response.status_code == 200
    expected = {
        "StudentId": 1000,
        "StudentName": "Al Jones",
        "CourseName": "Commerce",
        "UnitsToComplete": [],
    }
    assert response.json() == expected
    assert client.get("/StudentEnrolments/1000/Commerce").json() == expected


def test_put_only_changes_the_named_course(client):
    add(ALAN)
    add(ALAN_LAW)
    units = [{"UnitId": 62, "UnitName": "Criminal law"}]
    response = client.put(
        "/StudentEnrolments/1000/Law",
        json={"StudentName": "Alan Jones", "UnitsToComplete": units},
    )
    assert response.status_code == 200
    assert client.get("/StudentEnrolments/1000/Law").json()["UnitsToComplete"] == units
    assert client.get("/StudentEnrolments/1000/Commerce").json() == ALAN


def test_put_returns_404_when_missing(client):
    add(ALAN)
    response = client.put("/StudentEnrolments/1000/Law", json={"StudentName": "Alan"})
    assert response.status_code == 404


def test_put_returns_409_on_student_name_used_by_another_student(client):
    add(ALAN)
    add(MEI)
    response = client.put(
        "/StudentEnrolments/1003/Nursing", json={"StudentName": "Alan Jones"}
    )
    assert response.status_code == 409


def test_put_returns_409_on_name_mismatch_with_other_courses(client):
    add(ALAN)
    add(ALAN_LAW)
    response = client.put(
        "/StudentEnrolments/1000/Law", json={"StudentName": "Al Jones"}
    )
    assert response.status_code == 409


def test_put_keeping_own_name_is_not_a_conflict(client):
    add(ALAN)
    add(ALAN_LAW)
    body = {k: v for k, v in ALAN.items() if k not in ("StudentId", "CourseName")}
    response = client.put("/StudentEnrolments/1000/Commerce", json=body)
    assert response.status_code == 200


def test_put_returns_422_on_invalid_input(client):
    add(ALAN)
    response = client.put("/StudentEnrolments/1000/Commerce", json={})
    assert response.status_code == 422


# DELETE /StudentEnrolments/{id}/{courseName}


def test_delete_returns_204_and_keeps_other_courses(client):
    add(ALAN)
    add(ALAN_LAW)
    response = client.delete("/StudentEnrolments/1000/Commerce")
    assert response.status_code == 204
    assert [r.CourseName for r in Record.query(1000)] == ["Law"]


def test_delete_returns_404_when_missing(client):
    add(ALAN)
    assert client.delete("/StudentEnrolments/1000/Law").status_code == 404
