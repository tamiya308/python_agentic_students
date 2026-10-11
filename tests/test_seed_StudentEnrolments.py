from src.db import StudentEnrolmentRecord as Record
from src.seeds.seed_StudentEnrolments import SAMPLE_ENROLMENTS, seed


def test_seed_adds_five_records_to_empty_table(db):
    assert seed() == 5
    assert Record.count() == len(SAMPLE_ENROLMENTS) == 5


def test_seed_skips_when_table_has_data(db):
    Record(StudentId=1, StudentName="Existing").save()
    assert seed() == 0
    assert Record.count() == 1
