# utils/decorators.py
# Role-based access control decorators.

from functools import wraps


def role_required(allowed_roles):
    """
    Generic role-based decorator.
    Ensures the current user has one of the allowed roles.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):
            if not current_user:
                print("Access denied. Please login first.")
                return None

            if current_user.role not in allowed_roles:
                print("Access denied. Insufficient permissions.")
                return None

            return func(self, current_user, *args, **kwargs)

        return wrapper
    return decorator


# Specific decorators for cleaner usage

def admin_required(func):
    return role_required(["admin"])(func)


def health_worker_required(func):
    return role_required(["health_worker", "admin"])(func)


def community_required(func):
    return role_required(["community"])(func)
