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


def test_get_all_returns_200_ordered_by_student_id(client):
    add(MEI)
    add(ALAN)
    response = client.get("/StudentEnrolments")
    assert response.status_code == 200
    assert [e["StudentId"] for e in response.json()] == [1000, 1003]


def test_get_all_returns_200_empty_list(client):
    response = client.get("/StudentEnrolments")
    assert response.status_code == 200
    assert response.json() == []


# GET /StudentEnrolments/{id}


def test_get_one_returns_200(client):
    add(ALAN)
    response = client.get("/StudentEnrolments/1000")
    assert response.status_code == 200
    assert response.json() == ALAN


def test_get_one_returns_404_when_missing(client):
    assert client.get("/StudentEnrolments/9999").status_code == 404


# POST /StudentEnrolments


def test_post_returns_201_with_created_record(client):
    response = client.post("/StudentEnrolments", json=ALAN)
    assert response.status_code == 201
    assert response.json() == ALAN
    assert Record.get(1000).StudentName == "Alan Jones"


def test_post_returns_409_on_duplicate_student_id(client):
    add(ALAN)
    response = client.post(
        "/StudentEnrolments", json={**ALAN, "StudentName": "Someone Else"}
    )
    assert response.status_code == 409


def test_post_returns_409_on_duplicate_student_name(client):
    add(ALAN)
    response = client.post("/StudentEnrolments", json={**ALAN, "StudentId": 2000})
    assert response.status_code == 409


@pytest.mark.parametrize(
    "body",
    [
        {k: v for k, v in ALAN.items() if k != "StudentName"},
        {**ALAN, "StudentId": "not-a-number"},
        {**ALAN, "UnitsToComplete": [{"UnitId": 20}]},
    ],
)
def test_post_returns_422_on_invalid_input(client, body):
    assert client.post("/StudentEnrolments", json=body).status_code == 422


# PUT /StudentEnrolments/{id}


def test_put_returns_200_and_replaces_whole_record(client):
    add(ALAN)
    response = client.put("/StudentEnrolments/1000", json={"StudentName": "Al Jones"})
    assert response.status_code == 200
    expected = {
        "StudentId": 1000,
        "StudentName": "Al Jones",
        "CourseName": None,
        "UnitsToComplete": [],
    }
    assert response.json() == expected
    assert client.get("/StudentEnrolments/1000").json() == expected


def test_put_returns_404_when_missing(client):
    response = client.put("/StudentEnrolments/9999", json={"StudentName": "Nobody"})
    assert response.status_code == 404


def test_put_returns_409_on_duplicate_student_name(client):
    add(ALAN)
    add(MEI)
    response = client.put("/StudentEnrolments/1003", json={"StudentName": "Alan Jones"})
    assert response.status_code == 409


def test_put_keeping_own_name_is_not_a_conflict(client):
    add(ALAN)
    response = client.put("/StudentEnrolments/1000", json={**ALAN, "CourseName": "Law"})
    assert response.status_code == 200


def test_put_returns_422_on_invalid_input(client):
    add(ALAN)
    response = client.put("/StudentEnrolments/1000", json={"CourseName": "Law"})
    assert response.status_code == 422


# DELETE /StudentEnrolments/{id}


def test_delete_returns_204(client):
    add(ALAN)
    response = client.delete("/StudentEnrolments/1000")
    assert response.status_code == 204
    assert Record.count(1000) == 0


def test_delete_returns_404_when_missing(client):
    assert client.delete("/StudentEnrolments/9999").status_code == 404
