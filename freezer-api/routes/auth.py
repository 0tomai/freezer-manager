from flask import Blueprint, request, jsonify
from services.auth_service import verify_pin, generate_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    pin = data.get("pin", "")

    if not verify_pin(str(pin)):
        return jsonify({"error": "PIN incorrect."}), 401

    token = generate_token()
    return jsonify({"token": token}), 200
