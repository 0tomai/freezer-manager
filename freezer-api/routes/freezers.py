from flask import Blueprint, request, jsonify
from app import db
from models import Freezer
from utils.validators import require_json

freezers_bp = Blueprint("freezers", __name__)


@freezers_bp.get("/")
def list_freezers():
    freezers = Freezer.query.order_by(Freezer.created_at).all()
    return jsonify([f.to_dict(include_compartments=True) for f in freezers])


@freezers_bp.get("/<int:freezer_id>")
def get_freezer(freezer_id):
    freezer = Freezer.query.get_or_404(freezer_id)
    return jsonify(freezer.to_dict(include_compartments=True))


@freezers_bp.post("/")
@require_json("name")
def create_freezer():
    data = request.get_json()
    freezer = Freezer(
        name=data["name"].strip(),
        description=data.get("description", "").strip() or None,
        icon=data.get("icon", "🧊"),
    )
    db.session.add(freezer)
    db.session.commit()
    return jsonify(freezer.to_dict()), 201


@freezers_bp.put("/<int:freezer_id>")
@require_json("name")
def update_freezer(freezer_id):
    freezer = Freezer.query.get_or_404(freezer_id)
    data = request.get_json()
    freezer.name = data["name"].strip()
    freezer.description = data.get("description", freezer.description)
    freezer.icon = data.get("icon", freezer.icon)
    db.session.commit()
    return jsonify(freezer.to_dict())


@freezers_bp.delete("/<int:freezer_id>")
def delete_freezer(freezer_id):
    freezer = Freezer.query.get_or_404(freezer_id)
    db.session.delete(freezer)
    db.session.commit()
    return "", 204
