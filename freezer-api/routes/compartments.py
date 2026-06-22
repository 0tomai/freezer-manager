from flask import Blueprint, request, jsonify
from app import db
from models import Compartment, Freezer
from utils.validators import require_json

compartments_bp = Blueprint("compartments", __name__)


@compartments_bp.get("/freezer/<int:freezer_id>")
def list_compartments(freezer_id):
    Freezer.query.get_or_404(freezer_id)
    comps = (
        Compartment.query.filter_by(freezer_id=freezer_id)
        .order_by(Compartment.position)
        .all()
    )
    return jsonify([c.to_dict(include_items=True) for c in comps])


@compartments_bp.get("/<int:comp_id>")
def get_compartment(comp_id):
    comp = Compartment.query.get_or_404(comp_id)
    return jsonify(comp.to_dict(include_items=True))


@compartments_bp.post("/")
@require_json("freezer_id", "name")
def create_compartment():
    data = request.get_json()
    Freezer.query.get_or_404(data["freezer_id"])

    max_pos = db.session.query(
        db.func.max(Compartment.position)
    ).filter_by(freezer_id=data["freezer_id"]).scalar() or -1

    comp = Compartment(
        freezer_id=data["freezer_id"],
        name=data["name"].strip(),
        position=data.get("position", max_pos + 1),
    )
    db.session.add(comp)
    db.session.commit()
    return jsonify(comp.to_dict()), 201


@compartments_bp.put("/<int:comp_id>")
@require_json("name")
def update_compartment(comp_id):
    comp = Compartment.query.get_or_404(comp_id)
    data = request.get_json()
    comp.name = data["name"].strip()
    comp.position = data.get("position", comp.position)
    db.session.commit()
    return jsonify(comp.to_dict())


@compartments_bp.delete("/<int:comp_id>")
def delete_compartment(comp_id):
    comp = Compartment.query.get_or_404(comp_id)
    db.session.delete(comp)
    db.session.commit()
    return "", 204
