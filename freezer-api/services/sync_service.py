from datetime import datetime, timezone
from app import db
from models import Item, Compartment


def apply_sync_batch(operations: list) -> dict:
    """
    Traite une liste d'opérations offline en appliquant last-write-wins
    basé sur le champ `client_updated_at` fourni par le client.

    Format d'une opération :
    {
        "type": "upsert" | "delete",
        "entity": "item" | "compartment",
        "data": { ...fields... },
        "client_updated_at": "ISO8601"
    }
    """
    results = {"applied": 0, "skipped": 0, "errors": []}

    for op in operations:
        try:
            _apply_operation(op, results)
        except Exception as e:
            results["errors"].append({"op": op, "error": str(e)})

    db.session.commit()
    return results


def _apply_operation(op: dict, results: dict):
    op_type = op.get("type")
    entity = op.get("entity")
    data = op.get("data", {})
    client_ts = _parse_ts(op.get("client_updated_at"))

    if entity == "item":
        _sync_item(op_type, data, client_ts, results)
    elif entity == "compartment":
        _sync_compartment(op_type, data, client_ts, results)
    else:
        results["errors"].append({"op": op, "error": f"Entité inconnue : {entity}"})


def _sync_item(op_type, data, client_ts, results):
    item_id = data.get("id")
    item = Item.query.get(item_id) if item_id else None

    if op_type == "delete":
        if item:
            if client_ts is None or item.updated_at <= client_ts:
                db.session.delete(item)
                results["applied"] += 1
            else:
                results["skipped"] += 1
        return

    if op_type == "upsert":
        if item:
            if client_ts is None or item.updated_at <= client_ts:
                item.name = data.get("name", item.name)
                item.quantity = data.get("quantity", item.quantity)
                item.unit = data.get("unit", item.unit)
                item.notes = data.get("notes", item.notes)
                item.updated_at = datetime.now(timezone.utc)
                results["applied"] += 1
            else:
                results["skipped"] += 1
        else:
            new_item = Item(
                compartment_id=data["compartment_id"],
                name=data["name"],
                quantity=data.get("quantity", 1.0),
                unit=data.get("unit"),
                notes=data.get("notes"),
            )
            db.session.add(new_item)
            results["applied"] += 1


def _sync_compartment(op_type, data, client_ts, results):
    comp_id = data.get("id")
    comp = Compartment.query.get(comp_id) if comp_id else None

    if op_type == "delete":
        if comp:
            if client_ts is None or comp.updated_at <= client_ts:
                db.session.delete(comp)
                results["applied"] += 1
            else:
                results["skipped"] += 1
        return

    if op_type == "upsert":
        if comp:
            if client_ts is None or comp.updated_at <= client_ts:
                comp.name = data.get("name", comp.name)
                comp.position = data.get("position", comp.position)
                comp.updated_at = datetime.now(timezone.utc)
                results["applied"] += 1
            else:
                results["skipped"] += 1
        else:
            new_comp = Compartment(
                freezer_id=data["freezer_id"],
                name=data["name"],
                position=data.get("position", 0),
            )
            db.session.add(new_comp)
            results["applied"] += 1


def _parse_ts(ts_string):
    if not ts_string:
        return None
    try:
        dt = datetime.fromisoformat(ts_string.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None
