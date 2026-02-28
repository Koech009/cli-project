# models/case.py
# Represents a disease outbreak case

class Case:
    """
    Represents a reported outbreak case.

    Relationships:
    - Many cases belong to one Region (region_id)
    - Many cases reported by one User (reported_by)
    """

    VALID_STATUSES = ["suspected", "confirmed", "recovered"]

    def __init__(
        self,
        id: str,
        patient_name: str,
        age: int,
        region_id: str,
        status: str,
        reported_by: str,
        date_reported: str,
        disease: str
    ):
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of {self.VALID_STATUSES}"
            )

        self.id = id
        self.patient_name = patient_name
        self.age = age
        self.region_id = region_id
        self.status = status
        self.reported_by = reported_by
        self.date_reported = date_reported
        self.disease = disease

    def update_status(self, new_status: str):
        """
        Update case status.
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of {self.VALID_STATUSES}"
            )
        self.status = new_status

    def to_dict(self) -> dict:
        """
        Convert Case object to dictionary.
        """
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "region_id": self.region_id,
            "status": self.status,
            "reported_by": self.reported_by,
            "date_reported": self.date_reported,
            "disease": self.disease
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create Case object from dictionary.
        """
        return cls(
            id=data["id"],
            patient_name=data["patient_name"],
            age=data["age"],
            region_id=data["region_id"],
            status=data["status"],
            reported_by=data["reported_by"],
            date_reported=data["date_reported"],
            disease=data.get("disease", "Unknown")
        )

    def __str__(self):
        return (
            f"Case[{self.id}] - {self.patient_name}, "
            f"{self.disease}, {self.status} ({self.date_reported})"
        )
