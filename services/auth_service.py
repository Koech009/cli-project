# services/auth_service.py
# Handles user registration, login, and password hashing.

import uuid
from models.user import User
from utils.file_handler import load_json, save_json
from utils.validators import (
    validate_non_empty,
    validate_email,
    validate_password_strength,
    validate_role
)

USERS_FILE = "data/users.json"


class AuthService:
    """
    Handles authentication logic:
    - User registration
    - User login
    - Password hashing
    """

    def __init__(self):
        self.users = self._load_users()

    # ----------------------------
    # Internal Utility Methods
    # ----------------------------

    def _load_users(self):
        """
        Load users from JSON file and convert to User objects.
        """
        data = load_json(USERS_FILE)
        return [User.from_dict(user) for user in data]

    def _save_users(self):
        """
        Save current users list to JSON file.
        """
        data = [user.to_dict() for user in self.users]
        save_json(USERS_FILE, data)

    def _email_exists(self, email: str) -> bool:
        """
        Check if email is already registered.
        """
        return any(user.email == email for user in self.users)

    # ----------------------------
    # Public Methods
    # ----------------------------

    def register(self):
        """
        Register a new user with validation.
        """
        try:
            name = input("Enter name: ")
            validate_non_empty(name, "Name")

            email = input("Enter email: ")
            validate_email(email)

            if self._email_exists(email):
                raise ValueError("Email already registered.")

            password = input("Enter password: ")
            validate_password_strength(password)

            role = input("Enter role (community/health_worker/admin): ")
            validate_role(role)

            region_id = None
            if role == "health_worker":
                region_id = input(
                    "Enter region ID (optional): ").strip() or None

            # Create user and hash password using User helper
            new_user = User(
                id=str(uuid.uuid4()),
                name=name,
                email=email,
                password="",  # will be set below
                role=role,
                region_id=region_id
            )
            new_user.set_password(password)

            self.users.append(new_user)
            self._save_users()

            print("User registered successfully.")

        except ValueError as e:
            print(f"Registration failed: {e}")

    def login(self):
        """
        Authenticate user.
        Returns User object if successful.
        """
        try:
            email = input("Enter email: ")
            password = input("Enter password: ")

            for user in self.users:
                if user.email == email and user.verify_password(password):
                    print("Login successful.")
                    return user

            raise ValueError("Invalid email or password.")

        except ValueError as e:
            print(f"Login failed: {e}")
            return None
