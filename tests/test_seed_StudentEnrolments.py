import pytest

from src.db import StudentEnrolmentRecord as Record
from src.seeds import seed_StudentEnrolments_DEV, seed_StudentEnrolments_LOCAL

SEED_MODULES = [seed_StudentEnrolments_LOCAL, seed_StudentEnrolments_DEV]


@pytest.mark.parametrize("module", SEED_MODULES, ids=["LOCAL", "DEV"])
def test_seed_adds_five_records_to_empty_table(db, module):
    assert module.seed() == 5
    assert Record.count() == len(module.SAMPLE_ENROLMENTS) == 5


@pytest.mark.parametrize("module", SEED_MODULES, ids=["LOCAL", "DEV"])
def test_seed_skips_when_table_has_data(db, module):
    Record(StudentId=1, StudentName="Existing").save()
    assert module.seed() == 0
    assert Record.count() == 1


def test_local_and_dev_seed_data_differ():
    local_ids = {r["StudentId"] for r in seed_StudentEnrolments_LOCAL.SAMPLE_ENROLMENTS}
    dev_ids = {r["StudentId"] for r in seed_StudentEnrolments_DEV.SAMPLE_ENROLMENTS}
    assert local_ids.isdisjoint(dev_ids)
