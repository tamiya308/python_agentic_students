"""Seed the local (DynamoDB Local) StudentEnrolments table with sample data if it is empty.

Run on demand from the project root: .\\tools\\SeedData.ps1
"""

from src.config import load_env
from src.db import StudentEnrolmentRecord, configure_db, create_table_if_missing

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
        "StudentId": 1000,
        "StudentName": "Alan Jones",
        "CourseName": "Data Science",
        "UnitsToComplete": [
            {"UnitId": 90, "UnitName": "Statistics for data science"},
        ],
    },
    {
        "StudentId": 1000,
        "StudentName": "Alan Jones",
        "CourseName": "Law",
        "UnitsToComplete": [
            {"UnitId": 60, "UnitName": "Contract law"},
            {"UnitId": 61, "UnitName": "Legal research and writing"},
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
        "StudentId": 1001,
        "StudentName": "Priya Sharma",
        "CourseName": "Mathematics",
        "UnitsToComplete": [
            {"UnitId": 35, "UnitName": "Linear algebra"},
            {"UnitId": 36, "UnitName": "Calculus"},
        ],
    },
    {
        "StudentId": 1001,
        "StudentName": "Priya Sharma",
        "CourseName": "Physics",
        "UnitsToComplete": [
            {"UnitId": 37, "UnitName": "Mechanics"},
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


def seed() -> int:
    """Insert the sample records if the table has no data. Returns items added."""
    if next(iter(StudentEnrolmentRecord.scan(limit=1)), None) is not None:
        return 0
    with StudentEnrolmentRecord.batch_write() as batch:
        for item in SAMPLE_ENROLMENTS:
            batch.save(StudentEnrolmentRecord(**item))
    return len(SAMPLE_ENROLMENTS)


def main():
    load_env()
    configure_db()
    create_table_if_missing()
    added = seed()
    if added:
        print(f"Seeded {added} StudentEnrolments records.")
    else:
        print("StudentEnrolments already has data; nothing seeded.")


if __name__ == "__main__":
    main()
