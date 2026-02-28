# tests/test_case_service.py
import pytest
import uuid
from services.case_service import CaseService
from models.user import User


@pytest.fixture
def case_service(tmp_path, monkeypatch):
    # Override CASES_FILE to use a temp file
    from services import case_service as module
    module.CASES_FILE = tmp_path / "cases.json"
    return CaseService()


@pytest.fixture
def health_worker():
    return User(str(uuid.uuid4()), "HW", "hw@example.com", "hashed_pw", "health_worker")


def test_add_case_success(case_service, health_worker, monkeypatch):
    inputs = iter(["Patient A", "30", "region1", "suspected"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    case_service.add_case(health_worker)
    assert len(case_service.cases) == 1
    assert case_service.cases[0].status == "suspected"


def test_add_case_invalid_status(case_service, health_worker, monkeypatch, capsys):
    inputs = iter(["Patient B", "25", "region2", "invalid"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    case_service.add_case(health_worker)
    captured = capsys.readouterr()
    assert "Failed to add case" in captured.out


def test_update_case_status(case_service, health_worker, monkeypatch):
    # Add a case first
    inputs = iter(["Patient C", "40", "region3", "suspected"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    case_service.add_case(health_worker)

    # Update status
    inputs = iter([case_service.cases[0].id, "confirmed"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    case_service.update_case_status()
    assert case_service.cases[0].status == "confirmed"


def test_view_cases_empty(case_service, capsys):
    case_service.view_cases()
    captured = capsys.readouterr()
    assert "No cases found" in captured.out
