# utils/validators.py
# Contains all input validation functions for the system.

import re

# Centralized constants for consistency across models and services
VALID_ROLES = ["community", "health_worker", "admin"]

# Outbreak classification statuses
VALID_CLASSIFICATIONS = ["suspected", "confirmed", "discarded"]

# Patient outcome statuses
VALID_PATIENT_STATUSES = ["under_treatment", "recovered", "deceased"]


def validate_non_empty(value: str, field_name: str = "Field") -> None:
    """Ensures that a string is not empty."""
    if not value or value.strip() == "":
        raise ValueError(f"{field_name} cannot be empty.")


def validate_email(email: str) -> None:
    """Validates email format using regex."""
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format.")


def validate_password_strength(password: str) -> None:
    """Validates password strength."""
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("Password must contain at least one letter.")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one number.")


def validate_age(age: int) -> None:
    """Ensures age is a valid positive integer."""
    if not isinstance(age, int):
        raise ValueError("Age must be a number.")
    if age <= 0 or age > 120:
        raise ValueError("Age must be between 1 and 120.")


def validate_role(role: str) -> None:
    """Validates system roles."""
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role. Must be one of {VALID_ROLES}")


def validate_classification_status(status: str) -> None:
    """Validates outbreak classification status."""
    if status not in VALID_CLASSIFICATIONS:
        raise ValueError(
            f"Invalid classification status. Must be one of {VALID_CLASSIFICATIONS}")


def validate_patient_status(status: str) -> None:
    """Validates patient outcome status."""
    if status not in VALID_PATIENT_STATUSES:
        raise ValueError(
            f"Invalid patient status. Must be one of {VALID_PATIENT_STATUSES}")


def validate_region_name(name: str) -> None:
    """Ensures region name is valid and not too short."""
    validate_non_empty(name, "Region name")
    if len(name) < 3:
        raise ValueError("Region name must be at least 3 characters long.")
