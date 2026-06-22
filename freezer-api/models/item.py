from app import db
from datetime import datetime, timezone


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    compartment_id = db.Column(
        db.Integer, db.ForeignKey("compartments.id"), nullable=False
    )
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit = db.Column(db.String(30), nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "compartment_id": self.compartment_id,
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "notes": self.notes,
            "added_at": self.added_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
