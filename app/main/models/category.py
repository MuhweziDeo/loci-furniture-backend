from .. import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "name": self.name,
            "created": str(self.created),
            "id": self.id,
            "updated": str(self.updated)
        }
