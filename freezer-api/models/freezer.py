from app import db
from datetime import datetime, timezone


class Freezer(db.Model):
    __tablename__ = "freezers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(10), nullable=True, default="🧊")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    compartments = db.relationship(
        "Compartment", backref="freezer", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self, include_compartments=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_compartments:
            data["compartments"] = [c.to_dict() for c in self.compartments]
        return data
