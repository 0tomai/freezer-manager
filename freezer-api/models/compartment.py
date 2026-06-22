from app import db
from datetime import datetime, timezone


class Compartment(db.Model):
    __tablename__ = "compartments"

    id = db.Column(db.Integer, primary_key=True)
    freezer_id = db.Column(db.Integer, db.ForeignKey("freezers.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    items = db.relationship(
        "Item", backref="compartment", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self, include_items=False):
        data = {
            "id": self.id,
            "freezer_id": self.freezer_id,
            "name": self.name,
            "position": self.position,
            "updated_at": self.updated_at.isoformat(),
        }
        if include_items:
            data["items"] = [i.to_dict() for i in self.items]
        return data
