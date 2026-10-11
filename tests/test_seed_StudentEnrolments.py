import pytest

from src.db import StudentEnrolmentRecord as Record
from src.seeds import seed_StudentEnrolments_DEV, seed_StudentEnrolments_LOCAL

SEED_MODULES = [seed_StudentEnrolments_LOCAL, seed_StudentEnrolments_DEV]


@pytest.mark.parametrize("module", SEED_MODULES, ids=["LOCAL", "DEV"])
def test_seed_adds_every_item_to_empty_table(db, module):
    assert module.seed() == len(module.SAMPLE_ENROLMENTS) == 9
    assert Record.count() == 9


@pytest.mark.parametrize("module", SEED_MODULES, ids=["LOCAL", "DEV"])
def test_seed_has_five_students_with_some_in_three_courses(module):
    courses_per_student = {}
    for r in module.SAMPLE_ENROLMENTS:
        courses_per_student.setdefault(r["StudentId"], set()).add(r["CourseName"])
    assert len(courses_per_student) == 5
    assert sum(len(c) == 3 for c in courses_per_student.values()) == 2


@pytest.mark.parametrize("module", SEED_MODULES, ids=["LOCAL", "DEV"])
def test_seed_student_name_is_consistent_across_courses(module):
    names = {}
    for r in module.SAMPLE_ENROLMENTS:
        names.setdefault(r["StudentId"], set()).add(r["StudentName"])
    assert all(len(n) == 1 for n in names.values())


@pytest.mark.parametrize("module", SEED_MODULES, ids=["LOCAL", "DEV"])
def test_seed_skips_when_table_has_data(db, module):
    Record(StudentId=1, CourseName="Law", StudentName="Existing").save()
    assert module.seed() == 0
    assert Record.count() == 1


def test_local_and_dev_seed_data_differ():
    local_ids = {r["StudentId"] for r in seed_StudentEnrolments_LOCAL.SAMPLE_ENROLMENTS}
    dev_ids = {r["StudentId"] for r in seed_StudentEnrolments_DEV.SAMPLE_ENROLMENTS}
    assert local_ids.isdisjoint(dev_ids)
