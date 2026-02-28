# tests/test_case.py
import pytest
from models.case import Case


def test_case_creation_valid_status():
    case = Case("1", "Patient A", 30, "region1",
                "suspected", "user1", "2026-02-28")
    assert case.status == "suspected"


def test_case_invalid_status():
    with pytest.raises(ValueError):
        Case("2", "Patient B", 25, "region2", "invalid", "user2", "2026-02-28")


def test_update_case_status():
    case = Case("3", "Patient C", 40, "region3",
                "suspected", "user3", "2026-02-28")
    case.update_status("confirmed")
    assert case.status == "confirmed"


def test_case_to_dict_and_from_dict():
    case = Case("4", "Patient D", 50, "region4",
                "recovered", "user4", "2026-02-28")
    data = case.to_dict()
    new_case = Case.from_dict(data)
    assert new_case.patient_name == "Patient D"
    assert new_case.status == "recovered"
