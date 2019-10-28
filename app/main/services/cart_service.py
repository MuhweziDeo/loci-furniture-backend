from app.main.models.cart import Cart 
from .. import db


def get_all_carts():
	return Cart.query.all()


def get_user_cart(user_id):
	carts = Cart.query.filter_by(user_id=user_id).all()
	return carts

def find_product_in_cart(user_id, product_id):
	cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
	return cart	

def create_cart(data):
	cart = Cart(
		user_id= data["user_id"],
		product_id = data["product_id"],
		quantity=data["quantity"]
		)

	db.session.add(cart)
	db.session.commit()
	return cart

def update_cart(cart, data):
	cart.quantity = data["quantity"]
	db.session.add(cart)
	db.session.commit()
	return cart
	

def delete_cart(cart):
	db.session.delete(cart)
	db.session.commit()
	return cart	

def find_cart_by_id(cart_id):
	return Cart.query.filter_by(id=cart_id).first()	

