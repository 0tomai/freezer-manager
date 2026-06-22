from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError


def require_token(fn):
    """Décorateur : protège une route avec JWT."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except (JWTExtendedException, PyJWTError):
            return jsonify({"error": "Token invalide ou expiré."}), 401
        return fn(*args, **kwargs)
    return wrapper
