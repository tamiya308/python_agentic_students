import pytest

from src.db import StudentEnrolmentRecord as Record
from src.db import delete_table_if_exists
from src.drop_StudentEnrolments import check_target


def test_delete_table_if_exists_drops_the_table(db):
    Record(StudentId=1, CourseName="Law", StudentName="Existing").save()
    assert delete_table_if_exists() is True
    assert not Record.exists()


def test_delete_table_if_exists_returns_false_when_missing(db):
    Record.delete_table()
    assert delete_table_if_exists() is False


def test_check_target_local_refuses_without_dynamodb_url(monkeypatch):
    monkeypatch.delenv("DynamoDbUrl", raising=False)
    with pytest.raises(SystemExit):
        check_target("local")


def test_check_target_dev_refuses_with_dynamodb_url(monkeypatch):
    monkeypatch.setenv("DynamoDbUrl", "http://localhost:8000")
    with pytest.raises(SystemExit):
        check_target("dev")


def test_check_target_allows_matching_env(monkeypatch):
    monkeypatch.setenv("DynamoDbUrl", "http://localhost:8000")
    check_target("local")
    monkeypatch.delenv("DynamoDbUrl")
    check_target("dev")
