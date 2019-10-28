from .. import db, ma
from datetime import datetime
from .products import ProductSchema


class Cart(db.Model):
	__tablename__ = "cart"

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=1)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	created = db.Column(db.DateTime, default=datetime.utcnow())
	updated = db.Column(db.DateTime, default=datetime.utcnow())
	product = db.relationship('Product', backref='product', lazy=True)
	user = db.relationship("User", backref="user", lazy=True)

	def __str__(self):
		return "cart for {}".format(self.user_id)

	@property	
	def total(self):
		return self.product.price * self.quantity	

class CartSchema(ma.ModelSchema):
	product = ma.Nested(ProductSchema, required=True)
	class Meta:
		model = Cart
		fields = ("id","quantity", "product", "total")

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)		
