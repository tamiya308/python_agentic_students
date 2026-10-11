"""Seed the AWS dev StudentEnrolments table with sample data if it is empty.

Run on demand from the project root: .\\tools\\SeedData.ps1 -Env dev
"""

from src.config import load_env
from src.db import StudentEnrolmentRecord, configure_db, create_table_if_missing

SAMPLE_ENROLMENTS = [
    {
        "StudentId": 2000,
        "StudentName": "Hannah Becker",
        "CourseName": "Law",
        "UnitsToComplete": [
            {"UnitId": 60, "UnitName": "Contract law"},
            {"UnitId": 61, "UnitName": "Legal research and writing"},
        ],
    },
    {
        "StudentId": 2001,
        "StudentName": "Kwame Mensah",
        "CourseName": "Architecture",
        "UnitsToComplete": [
            {"UnitId": 70, "UnitName": "Design studio 1"},
            {"UnitId": 71, "UnitName": "History of architecture"},
        ],
    },
    {
        "StudentId": 2002,
        "StudentName": "Yuki Tanaka",
        "CourseName": "Psychology",
        "UnitsToComplete": [
            {"UnitId": 80, "UnitName": "Introduction to psychology"},
            {"UnitId": 81, "UnitName": "Research methods"},
        ],
    },
    {
        "StudentId": 2003,
        "StudentName": "Diego Alvarez",
        "CourseName": "Data Science",
        "UnitsToComplete": [
            {"UnitId": 90, "UnitName": "Statistics for data science"},
        ],
    },
    {
        "StudentId": 2004,
        "StudentName": "Fatima Al-Sayed",
        "CourseName": "Law",
        "UnitsToComplete": [
            {"UnitId": 60, "UnitName": "Contract law"},
            {"UnitId": 62, "UnitName": "Criminal law"},
        ],
    },
]


def seed() -> int:
    """Insert the sample records if the table has no data. Returns rows added."""
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
