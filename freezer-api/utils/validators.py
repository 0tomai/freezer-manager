from flask import request, abort


def require_json(*required_fields):
    """Decorator: vérifie que le body JSON contient les champs requis."""
    def decorator(fn):
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                abort(400, description="Le body doit être en JSON.")
            missing = [f for f in required_fields if f not in data or data[f] is None]
            if missing:
                abort(400, description=f"Champs manquants : {', '.join(missing)}")
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator


def validate_quantity(value):
    try:
        q = float(value)
        if q < 0:
            raise ValueError
        return q
    except (TypeError, ValueError):
        abort(400, description="La quantité doit être un nombre positif.")
