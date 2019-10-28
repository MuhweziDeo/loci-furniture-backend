from .. import db, ma
from datetime import datetime
from .category import CategorySchema


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_1 = db.Column(db.Text, nullable=False)
    image_2 = db.Column(db.Text, nullable=False)
    image_3 = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref="products", lazy=True, uselist=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return self.name        

    def serialze(self):
        return {
            "id": self.id,
            "image_1": self.image_1,
            "image_2": self.image_2,
            "image_3": self.image_3,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

class ProductSchema(ma.ModelSchema):
    category = ma.Nested(CategorySchema)
    class Meta:
        model = Product
        # fields = ("c",)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)