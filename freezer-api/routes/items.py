from flask import Blueprint, request, jsonify
from app import db
from models import Item, Compartment
from utils.validators import require_json, validate_quantity
from services.sync_service import apply_sync_batch

items_bp = Blueprint("items", __name__)


@items_bp.get("/compartment/<int:comp_id>")
def list_items(comp_id):
    Compartment.query.get_or_404(comp_id)
    items = Item.query.filter_by(compartment_id=comp_id).order_by(Item.name).all()
    return jsonify([i.to_dict() for i in items])


@items_bp.post("/")
@require_json("compartment_id", "name")
def create_item():
    data = request.get_json()
    Compartment.query.get_or_404(data["compartment_id"])
    quantity = validate_quantity(data.get("quantity", 1.0))

    item = Item(
        compartment_id=data["compartment_id"],
        name=data["name"].strip(),
        quantity=quantity,
        unit=data.get("unit", "").strip() or None,
        notes=data.get("notes", "").strip() or None,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@items_bp.put("/<int:item_id>")
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json(silent=True) or {}

    if "name" in data:
        item.name = data["name"].strip()
    if "quantity" in data:
        item.quantity = validate_quantity(data["quantity"])
    if "unit" in data:
        item.unit = data["unit"].strip() or None
    if "notes" in data:
        item.notes = data["notes"].strip() or None
    if "compartment_id" in data:
        Compartment.query.get_or_404(data["compartment_id"])
        item.compartment_id = data["compartment_id"]

    db.session.commit()
    return jsonify(item.to_dict())


@items_bp.patch("/<int:item_id>/quantity")
@require_json("delta")
def adjust_quantity(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()

    try:
        delta = float(data["delta"])
    except (TypeError, ValueError):
        return jsonify({"error": "delta doit être un nombre."}), 400

    new_qty = item.quantity + delta
    if new_qty < 0:
        return jsonify({"error": "La quantité ne peut pas être négative."}), 400

    item.quantity = new_qty
    db.session.commit()
    return jsonify(item.to_dict())


@items_bp.delete("/<int:item_id>")
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204


@items_bp.post("/sync")
def sync_offline():
    data = request.get_json(silent=True) or {}
    operations = data.get("operations", [])

    if not isinstance(operations, list):
        return jsonify({"error": "operations doit être une liste."}), 400

    result = apply_sync_batch(operations)
    return jsonify(result), 200
