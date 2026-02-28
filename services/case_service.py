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
    Handles case creation, updates, and retrieval.
    """

    def __init__(self):
        self.cases = self._load_cases()

    # ----------------------------
    # Internal Methods
    # ----------------------------

    def _load_cases(self):
        """
        Load cases from JSON and convert to Case objects.
        """
        data = load_json(CASES_FILE)
        return [Case.from_dict(case) for case in data]

    def _save_cases(self):
        """
        Save current cases to JSON file.
        """
        data = [case.to_dict() for case in self.cases]
        save_json(CASES_FILE, data)

    # ----------------------------
    # Public Methods
    # ----------------------------

    def add_case(self, current_user):
        """
        Add a new outbreak case.
        Only Health Worker or Admin can add cases.
        """
        try:
            if current_user.role not in ["health_worker", "admin"]:
                raise PermissionError(
                    "Only Health Worker or Admin can add cases."
                )

            patient_name = input("Patient name: ")
            validate_non_empty(patient_name, "Patient name")

            age = int(input("Age: "))
            validate_age(age)

            region_id = input("Region ID: ")
            validate_non_empty(region_id, "Region ID")

            disease = input("Disease name: ")   # NEW
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
                disease=disease
            )

            self.cases.append(new_case)
            self._save_cases()

            print("Case added successfully.")

        except (ValueError, PermissionError) as e:
            print(f"Failed to add case: {e}")

    def update_case_status(self):
        """
        Update status of an existing case.
        """
        try:
            case_id = input("Enter Case ID: ")
            new_status = input("New status: ")
            validate_status(new_status)

            for case in self.cases:
                if case.id == case_id:
                    case.update_status(new_status)
                    self._save_cases()
                    print("Case status updated.")
                    return

            raise ValueError("Case not found.")

        except ValueError as e:
            print(f"Update failed: {e}")

    def view_cases(self):
        """
        Display all cases in a Rich table.
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
        table.add_column("Disease", style="blue")   # NEW
        table.add_column("Status", style="red")
        table.add_column("Date Reported", style="white")

        for case in self.cases:
            table.add_row(
                case.id,
                case.patient_name,
                str(case.age),
                case.region_id,
                case.disease,
                case.status,
                case.date_reported
            )

        console.print(table)

    def get_cases_by_region(self, region_id: str):
        """
        Fetch cases belonging to a specific region.
        """
        return [case for case in self.cases if case.region_id == region_id]

    def generate_summary(self):
        """
        Generate a summary report of case statuses.
        """
        summary = {"suspected": 0, "confirmed": 0, "recovered": 0}
        for case in self.cases:
            if case.status in summary:
                summary[case.status] += 1
        return summary
