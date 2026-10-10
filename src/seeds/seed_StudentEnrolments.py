"""Seed the StudentEnrolments table with sample data if it is empty.

Run on demand from the project root: .\\tools\\SeedData.ps1
"""

from dotenv import load_dotenv

from src.db import create_table_if_missing, get_dynamodb_resource

SAMPLE_ENROLMENTS = [
    {
        "StudentId": 1000,
        "StudentName": "Alan Jones",
        "CourseName": "Commerce",
        "UnitsToComplete": [
            {"UnitId": 20, "UnitName": "Introduction to business"},
            {"UnitId": 21, "UnitName": "Managements basics"},
        ],
    },
    {
        "StudentId": 1001,
        "StudentName": "Priya Sharma",
        "CourseName": "Computer Science",
        "UnitsToComplete": [
            {"UnitId": 30, "UnitName": "Programming fundamentals"},
            {"UnitId": 31, "UnitName": "Data structures"},
        ],
    },
    {
        "StudentId": 1002,
        "StudentName": "Liam O'Connor",
        "CourseName": "Engineering",
        "UnitsToComplete": [
            {"UnitId": 40, "UnitName": "Engineering mathematics"},
            {"UnitId": 41, "UnitName": "Statics"},
        ],
    },
    {
        "StudentId": 1003,
        "StudentName": "Mei Chen",
        "CourseName": "Nursing",
        "UnitsToComplete": [
            {"UnitId": 50, "UnitName": "Anatomy and physiology"},
        ],
    },
    {
        "StudentId": 1004,
        "StudentName": "Sofia Rossi",
        "CourseName": "Commerce",
        "UnitsToComplete": [
            {"UnitId": 20, "UnitName": "Introduction to business"},
            {"UnitId": 22, "UnitName": "Accounting principles"},
        ],
    },
]


def seed(table) -> int:
    """Insert the sample records if the table has no data. Returns rows added."""
    if table.scan(Limit=1).get("Items"):
        return 0
    with table.batch_writer() as batch:
        for item in SAMPLE_ENROLMENTS:
            batch.put_item(Item=item)
    return len(SAMPLE_ENROLMENTS)


def main():
    load_dotenv()
    table = create_table_if_missing(get_dynamodb_resource())
    added = seed(table)
    if added:
        print(f"Seeded {added} StudentEnrolments records.")
    else:
        print("StudentEnrolments already has data; nothing seeded.")


if __name__ == "__main__":
    main()
