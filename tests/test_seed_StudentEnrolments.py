import boto3
import pytest
from moto import mock_aws

from src.db import create_table_if_missing
from src.seeds.seed_StudentEnrolments import SAMPLE_ENROLMENTS, seed


@pytest.fixture
def table(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
        yield create_table_if_missing(dynamodb)


def test_seed_adds_five_records_to_empty_table(table):
    assert seed(table) == 5
    assert len(table.scan()["Items"]) == len(SAMPLE_ENROLMENTS) == 5


def test_seed_skips_when_table_has_data(table):
    table.put_item(Item={"StudentId": 1, "StudentName": "Existing"})
    assert seed(table) == 0
    assert len(table.scan()["Items"]) == 1
