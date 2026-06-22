from flask import current_app
from flask_jwt_extended import create_access_token


def verify_pin(pin: str) -> bool:
    expected = current_app.config.get("SHARED_PIN", "1234")
    return pin == expected


def generate_token() -> str:
    return create_access_token(identity="shared_user")
