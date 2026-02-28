# models/case.py
# Represents a disease outbreak case

class Case:
    """
    Represents a reported outbreak case.

    Relationships:
    - Many cases belong to one Region (region_id)
    - Many cases reported by one User (reported_by)

    Fields:
    - symptoms: list of reported symptoms (community user)
    - possible_disease: suspected disease (community user)
    - confirmed_disease: verified disease (health worker)
    """

    VALID_STATUSES = ["pending", "suspected",
                      "confirmed", "recovered", "deceased"]

    def __init__(
        self,
        id: str,
        patient_name: str,
        age: int,
        region_id: str,
        status: str,
        reported_by: str,
        date_reported: str,
        symptoms=None,
        possible_disease=None,
        confirmed_disease=None
    ):
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of {self.VALID_STATUSES}")

        self.id = id
        self.patient_name = patient_name
        self.age = age
        self.region_id = region_id
        self.status = status
        self.reported_by = reported_by
        self.date_reported = date_reported
        self.symptoms = symptoms or []
        self.possible_disease = possible_disease
        self.confirmed_disease = confirmed_disease

    # ----------------------------
    # Helper Methods
    # ----------------------------

    def update_status(self, new_status: str):
        """Update case status with validation."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of {self.VALID_STATUSES}")
        self.status = new_status

    def confirm_disease(self, disease_name: str):
        """Health worker confirms suspected disease."""
        if not disease_name:
            raise ValueError("Confirmed disease name cannot be empty.")
        self.confirmed_disease = disease_name
        self.status = "confirmed"

    def to_dict(self) -> dict:
        """Convert Case object to dictionary for JSON storage."""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "region_id": self.region_id,
            "status": self.status,
            "reported_by": self.reported_by,
            "date_reported": self.date_reported,
            "symptoms": self.symptoms,
            "possible_disease": self.possible_disease,
            "confirmed_disease": self.confirmed_disease,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Recreate Case object from stored dictionary."""
        return cls(
            id=data["id"],
            patient_name=data["patient_name"],
            age=data["age"],
            region_id=data["region_id"],
            status=data["status"],
            reported_by=data["reported_by"],
            date_reported=data["date_reported"],
            symptoms=data.get("symptoms", []),
            possible_disease=data.get("possible_disease"),
            confirmed_disease=data.get("confirmed_disease"),
        )

    def __str__(self):
        return (
            f"Case[{self.id}] - {self.patient_name}, "
            f"Symptoms: {', '.join(self.symptoms) if self.symptoms else 'None'}, "
            f"Possible: {self.possible_disease or 'N/A'}, "
            f"Confirmed: {self.confirmed_disease or 'N/A'}, "
            f"Status: {self.status} ({self.date_reported})"
        )
