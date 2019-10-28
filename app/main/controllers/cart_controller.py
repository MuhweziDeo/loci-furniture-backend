import os
import json
from flask_restplus import Resource
from flask import request,jsonify
from ..utils.dto import CartDto
from ..utils.decorator import login_required, admin_required
from ..services import cart_service, product_service
from ..helpers.user_helper import get_logged_in_user
from ..models.cart import carts_schema, cart_schema

api = CartDto.api

@api.route("")
class UserCart(Resource):

	@login_required
	def get(self):
		current_user = get_logged_in_user()
		data = cart_service.get_user_cart(current_user["id"])
		return {
			"data": carts_schema.dump(data)
		}
	
	@api.expect(CartDto.cart, validate=True)	
	@login_required 
	def post(self):
		try:
			_body = request.json
			product_id = product_service.find_product_by_id(_body["product_id"])

			if product_id is None:
				return {
					"message": "Product Not Found",
					"success": False
				}, 404

			current_user = get_logged_in_user()
			has_added_to_cart = cart_service.find_product_in_cart(current_user["id"], _body["product_id"])

			if has_added_to_cart:
				return {
					"message": "Product Added to Cart Already",
					"success": False
				}, 400

			_body["user_id"] = current_user["id"]

			cart = cart_service.create_cart(_body)

			return {
				"data":  cart_schema.dump(cart)
			}
		except Exception as e:
			return {
					"message": str(e) or "Unable to add item to cart"
				}
	


@api.route("/<cart_id>")
class Cart(Resource):
	
	@login_required
	def delete(self, cart_id):
		current_user = get_logged_in_user()
		cart = cart_service.find_cart_by_id(cart_id)
		if cart is None:
			return {
				"message": "Cart Item Not Found",
				"success": False
			}, 404
		if not cart.user_id == current_user["id"]:
			return {
				"message": "Permission Denied",
				"success": False
			}, 401
		delete_cart = cart_service.delete_cart(cart)	
		return {
			"message": "Item Removed from cart",
			"success": True,
			"data": cart_schema.dump(delete_cart)
		}

	@login_required	
	def update(self, cart_id):
		current_user = get_logged_in_user()
		_json = request.json
		if not _json:
			return {
				"message": "Please provide atleast one value",
				"success": False
			}, 400
		cart = cart_service.find_cart_by_id(cart_id)
		if cart is None:
			return {
				"message": "Cart Item Not Found",
				"success": False
			}, 404
		if not cart.user_id == current_user["id"]:
			return {
				"message": "Permission Denied",
				"success": False
			}, 401
		delete_cart = cart_service.update_cart(cart, _json)	
		return {
			"message": "Item Removed from cart",
			"success": True,
			"data": cart_schema.dump(delete_cart)
		}							