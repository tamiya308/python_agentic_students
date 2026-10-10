import os

import boto3

TABLE_NAME = "StudentEnrolments"


def get_dynamodb_resource():
    """Create a boto3 DynamoDB resource from the DynamoDbUrl environment variable.

    When DynamoDbUrl is set (e.g. DynamoDB Local), dummy credentials and a default
    region are used unless the standard AWS_* variables are provided.
    """
    endpoint_url = os.getenv("DynamoDbUrl") or None
    kwargs = {"region_name": os.getenv("AWS_REGION", "ap-southeast-2")}
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "local")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "local")
    return boto3.resource("dynamodb", **kwargs)


def create_table_if_missing(dynamodb):
    """Create the StudentEnrolments table if it doesn't already exist."""
    existing = dynamodb.meta.client.list_tables()["TableNames"]
    if TABLE_NAME in existing:
        return dynamodb.Table(TABLE_NAME)
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "StudentId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "StudentId", "AttributeType": "N"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    return table


def get_table():
    """FastAPI dependency returning the StudentEnrolments table."""
    return get_dynamodb_resource().Table(TABLE_NAME)
