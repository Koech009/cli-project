import pytest
from models.case import Case


def test_case_creation_valid_status():
    case = Case(
        id="1",
        patient_name="Patient A",
        age=30,
        region_id="region1",
        classification_status="suspected",
        patient_status="under_treatment",
        reported_by="user1",
        date_reported="2026-02-28"
    )
    assert case.classification_status == "suspected"
    assert case.patient_status == "under_treatment"


def test_case_invalid_status():
    # Invalid classification status should raise
    with pytest.raises(ValueError):
        Case(
            id="2",
            patient_name="Patient B",
            age=25,
            region_id="region2",
            classification_status="invalid",
            patient_status="under_treatment",
            reported_by="user2",
            date_reported="2026-02-28"
        )


def test_update_case_status():
    case = Case(
        id="3",
        patient_name="Patient C",
        age=40,
        region_id="region3",
        classification_status="suspected",
        patient_status="under_treatment",
        reported_by="user3",
        date_reported="2026-02-28"
    )
    case.update_classification("confirmed")
    case.update_patient_status("recovered")
    assert case.classification_status == "confirmed"
    assert case.patient_status == "recovered"


def test_case_to_dict_and_from_dict():
    case = Case(
        id="4",
        patient_name="Patient D",
        age=50,
        region_id="region4",
        classification_status="confirmed",
        patient_status="deceased",
        reported_by="user4",
        date_reported="2026-02-28",
        confirmed_disease="Ebola"
    )
    data = case.to_dict()
    new_case = Case.from_dict(data)
    assert new_case.patient_name == "Patient D"
    assert new_case.classification_status == "confirmed"
    assert new_case.patient_status == "deceased"
    assert new_case.confirmed_disease == "Ebola"
