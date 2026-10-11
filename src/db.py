import os
import time

from pynamodb.attributes import (
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model

TABLE_NAME = "StudentEnrolments"


class UnitAttribute(MapAttribute):
    UnitId = NumberAttribute()
    UnitName = UnicodeAttribute()


class StudentEnrolmentRecord(Model):
    """PynamoDB mapping for the StudentEnrolments table: one item per student per course."""

    class Meta:
        table_name = TABLE_NAME
        region = "ap-southeast-2"
        billing_mode = "PAY_PER_REQUEST"

    StudentId = NumberAttribute(hash_key=True)
    CourseName = UnicodeAttribute(range_key=True)
    StudentName = UnicodeAttribute()
    UnitsToComplete = ListAttribute(of=UnitAttribute, default=list)


def configure_db():
    """Point the PynamoDB model at the DynamoDbUrl environment variable.

    Called after load_dotenv(). When DynamoDbUrl is set (e.g. DynamoDB Local),
    dummy credentials are used unless the standard AWS_* variables are provided.
    """
    meta = StudentEnrolmentRecord.Meta
    meta.host = os.getenv("DynamoDbUrl") or None
    meta.region = os.getenv("AWS_REGION", "ap-southeast-2")
    if meta.host:
        meta.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "local")
        meta.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "local")
    # Drop any cached connection so the new settings take effect.
    StudentEnrolmentRecord._connection = None


def create_table_if_missing():
    """Create the StudentEnrolments table if it doesn't already exist."""
    if not StudentEnrolmentRecord.exists():
        StudentEnrolmentRecord.create_table(wait=True)


def delete_table_if_exists() -> bool:
    """Delete the StudentEnrolments table and wait until it's gone.

    Returns False if the table didn't exist. Waiting matters on AWS, where a
    table stays in DELETING for a few seconds and can't be recreated until then.
    """
    if not StudentEnrolmentRecord.exists():
        return False
    StudentEnrolmentRecord.delete_table()
    while StudentEnrolmentRecord.exists():
        time.sleep(1)
    return True
