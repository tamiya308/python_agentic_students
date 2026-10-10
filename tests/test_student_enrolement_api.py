import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from src.db import create_table_if_missing
from src.main import app
from src.db import get_table

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


@pytest.fixture
def table(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
        yield create_table_if_missing(dynamodb)


@pytest.fixture
def client(table):
    # No `with` block, so the startup lifespan (real DynamoDB) doesn't run.
    app.dependency_overrides[get_table] = lambda: table
    yield TestClient(app)
    app.dependency_overrides.clear()


# GET /StudentEnrolments


def test_get_all_returns_200_ordered_by_student_id(client, table):
    table.put_item(Item=MEI)
    table.put_item(Item=ALAN)
    response = client.get("/StudentEnrolments")
    assert response.status_code == 200
    assert [e["StudentId"] for e in response.json()] == [1000, 1003]


def test_get_all_returns_200_empty_list(client):
    response = client.get("/StudentEnrolments")
    assert response.status_code == 200
    assert response.json() == []


# GET /StudentEnrolments/{id}


def test_get_one_returns_200(client, table):
    table.put_item(Item=ALAN)
    response = client.get("/StudentEnrolments/1000")
    assert response.status_code == 200
    assert response.json() == ALAN


def test_get_one_returns_404_when_missing(client):
    assert client.get("/StudentEnrolments/9999").status_code == 404


# POST /StudentEnrolments


def test_post_returns_201_with_created_record(client, table):
    response = client.post("/StudentEnrolments", json=ALAN)
    assert response.status_code == 201
    assert response.json() == ALAN
    assert table.get_item(Key={"StudentId": 1000})["Item"]["StudentName"] == (
        "Alan Jones"
    )


def test_post_returns_409_on_duplicate_student_id(client, table):
    table.put_item(Item=ALAN)
    response = client.post(
        "/StudentEnrolments", json={**ALAN, "StudentName": "Someone Else"}
    )
    assert response.status_code == 409


def test_post_returns_409_on_duplicate_student_name(client, table):
    table.put_item(Item=ALAN)
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


def test_put_returns_200_and_replaces_whole_record(client, table):
    table.put_item(Item=ALAN)
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


def test_put_returns_409_on_duplicate_student_name(client, table):
    table.put_item(Item=ALAN)
    table.put_item(Item=MEI)
    response = client.put("/StudentEnrolments/1003", json={"StudentName": "Alan Jones"})
    assert response.status_code == 409


def test_put_keeping_own_name_is_not_a_conflict(client, table):
    table.put_item(Item=ALAN)
    response = client.put("/StudentEnrolments/1000", json={**ALAN, "CourseName": "Law"})
    assert response.status_code == 200


def test_put_returns_422_on_invalid_input(client, table):
    table.put_item(Item=ALAN)
    response = client.put("/StudentEnrolments/1000", json={"CourseName": "Law"})
    assert response.status_code == 422


# DELETE /StudentEnrolments/{id}


def test_delete_returns_204(client, table):
    table.put_item(Item=ALAN)
    response = client.delete("/StudentEnrolments/1000")
    assert response.status_code == 204
    assert "Item" not in table.get_item(Key={"StudentId": 1000})


def test_delete_returns_404_when_missing(client):
    assert client.delete("/StudentEnrolments/9999").status_code == 404
