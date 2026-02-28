# services/case_service.py
# Handles outbreak case operations.

import uuid
from datetime import datetime
from rich.console import Console
from rich.table import Table
from models.case import Case
from utils.file_handler import load_json, save_json
from utils.validators import (
    validate_non_empty,
    validate_age,
    validate_status
)

CASES_FILE = "data/cases.json"


class CaseService:
    """
    Handles case creation, updates, deletion, and retrieval.
    """

    def __init__(self):
        self.cases = self._load_cases()

    # ----------------------------
    # Internal Methods
    # ----------------------------

    def _load_cases(self):
        """Load cases from JSON and convert to Case objects."""
        data = load_json(CASES_FILE)
        return [Case.from_dict(case) for case in data]

    def _save_cases(self):
        """Save current cases to JSON file."""
        data = [case.to_dict() for case in self.cases]
        save_json(CASES_FILE, data)

    def _find_case(self, case_id):
        """Helper: find a case by ID."""
        for case in self.cases:
            if case.id == case_id:
                return case
        return None

    # ----------------------------
    # Public Methods
    # ----------------------------

    def add_case(self, current_user):
        """
        Add a new outbreak case.
        - Community users: report suspected case (symptoms + possible disease).
        - Health workers/Admin: add confirmed case directly.
        """
        try:
            patient_name = input("Patient name: ")
            validate_non_empty(patient_name, "Patient name")

            age = int(input("Age: "))
            validate_age(age)

            region_id = input("Region ID: ")
            validate_non_empty(region_id, "Region ID")

            if current_user.role == "community":
                # Community reports suspected case
                symptoms = input("Symptoms (comma separated): ").split(",")
                symptoms = [s.strip() for s in symptoms if s.strip()]
                possible_disease = input(
                    "Possible disease (optional): ") or None

                new_case = Case(
                    id=str(uuid.uuid4()),
                    patient_name=patient_name,
                    age=age,
                    region_id=region_id,
                    status="pending",
                    reported_by=current_user.id,
                    date_reported=datetime.now().strftime("%Y-%m-%d"),
                    symptoms=symptoms,
                    possible_disease=possible_disease,
                    confirmed_disease=None
                )
            else:
                # Health worker/Admin adds confirmed case
                disease = input("Disease name: ")
                validate_non_empty(disease, "Disease name")

                status = input("Status (suspected/confirmed/recovered): ")
                validate_status(status)

                new_case = Case(
                    id=str(uuid.uuid4()),
                    patient_name=patient_name,
                    age=age,
                    region_id=region_id,
                    status=status,
                    reported_by=current_user.id,
                    date_reported=datetime.now().strftime("%Y-%m-%d"),
                    symptoms=[],
                    possible_disease=None,
                    confirmed_disease=disease
                )

            self.cases.append(new_case)
            self._save_cases()
            print("✅ Case added successfully.")

        except (ValueError, PermissionError) as e:
            print(f"❌ Failed to add case: {e}")

    def update_case_status(self, current_user):
        """
        Update status of an existing case.
        - Admin: any case
        - Health worker: their own cases or community cases they confirmed
        - Community: not allowed
        """
        try:
            if current_user.role == "community":
                raise PermissionError(
                    "Community users cannot update case status.")

            case_id = input("Enter Case ID: ")
            new_status = input("New status: ")
            validate_status(new_status)

            case = self._find_case(case_id)
            if not case:
                raise ValueError("Case not found.")

            if current_user.role == "health_worker" and case.reported_by != current_user.id:
                raise PermissionError(
                    "Health workers can only update their own or confirmed cases.")

            case.update_status(new_status)
            self._save_cases()
            print("✅ Case status updated.")

        except (ValueError, PermissionError) as e:
            print(f"❌ Update failed: {e}")

    def confirm_disease(self, current_user):
        """
        Health worker confirms suspected disease for a community case.
        """
        try:
            if current_user.role != "health_worker":
                raise PermissionError(
                    "Only health workers can confirm diseases.")

            case_id = input("Enter Case ID to confirm: ")
            disease = input("Confirmed disease: ")
            validate_non_empty(disease, "Confirmed disease")

            case = self._find_case(case_id)
            if not case:
                raise ValueError("Case not found.")

            case.confirmed_disease = disease
            case.status = "confirmed"
            self._save_cases()
            print("✅ Disease confirmed.")

        except (ValueError, PermissionError) as e:
            print(f"❌ Confirmation failed: {e}")

    def delete_case(self, current_user):
        """
        Delete a case with role-based rules:
        - Admin: can delete any case
        - Health worker: can delete only their own cases
        - Community: can delete only their own unconfirmed cases
        """
        try:
            case_id = input("Enter Case ID to delete: ")
            case = self._find_case(case_id)
            if not case:
                raise ValueError("Case not found.")

            if current_user.role == "admin":
                pass  # Admin can delete any case
            elif current_user.role == "health_worker":
                if case.reported_by != current_user.id:
                    raise PermissionError(
                        "Health workers can only delete their own cases.")
            elif current_user.role == "community":
                if case.reported_by != current_user.id or case.status != "pending":
                    raise PermissionError(
                        "Community users can only delete their own unconfirmed cases.")
            else:
                raise PermissionError("Invalid role.")

            self.cases = [c for c in self.cases if c.id != case_id]
            self._save_cases()
            print("✅ Case deleted successfully.")

        except (ValueError, PermissionError) as e:
            print(f"❌ Deletion failed: {e}")

    def view_cases(self, user=None):
        """
        Display cases in a Rich table.
        - Admin/Health worker: see all cases
        - Community: see only their own cases
        """
        console = Console()
        if not self.cases:
            console.print("[bold red]No cases found[/bold red]")
            return

        table = Table(title="Outbreak Cases")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Patient", style="magenta")
        table.add_column("Age", style="green")
        table.add_column("Region", style="yellow")
        table.add_column("Symptoms", style="blue")
        table.add_column("Possible Disease", style="blue")
        table.add_column("Confirmed Disease", style="blue")
        table.add_column("Status", style="red")
        table.add_column("Date Reported", style="white")

        for case in self.cases:
            if user and user.role == "community" and case.reported_by != user.id:
                continue  # Community users only see their own cases

            table.add_row(
                case.id,
                case.patient_name,
                str(case.age),
                case.region_id,
                ", ".join(case.symptoms) if case.symptoms else "-",
                case.possible_disease or "-",
                case.confirmed_disease or "-",
                case.status,
                case.date_reported
            )

        console.print(table)

    def get_cases_by_region(self, region_id: str):
        """Fetch cases belonging to a specific region."""
        return [case for case in self.cases if case.region_id == region_id]

    def generate_summary(self):
        """Generate a summary report of case statuses."""
        summary = {"pending": 0, "suspected": 0,
                   "confirmed": 0, "recovered": 0}
        for case in self.cases:
            if case.status in summary:
                summary[case.status] += 1
        return summary
