import pytest
from moto import mock_aws

from src.db import StudentEnrolmentRecord, configure_db, create_table_if_missing


@pytest.fixture
def db(monkeypatch):
    """Point the PynamoDB model at an in-memory Moto DynamoDB with the table created."""
    monkeypatch.delenv("DynamoDbUrl", raising=False)
    monkeypatch.setenv("AWS_REGION", "ap-southeast-2")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    with mock_aws():
        configure_db()
        create_table_if_missing()
        yield StudentEnrolmentRecord
    StudentEnrolmentRecord._connection = None
