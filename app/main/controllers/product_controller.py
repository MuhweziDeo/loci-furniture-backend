import os
from flask_restplus import Resource
from flask import request,jsonify
from ..utils.dto import ProductDto
from ..utils.decorator import admin_required
from ..utils.save_image import save_image
from ..services import product_service
from ..models.products import products_schema, product_schema
from werkzeug.utils import secure_filename
from werkzeug.exceptions import  BadRequestKeyError
from ..services import product_service, category_service

api = ProductDto.api
_product = ProductDto.product


@api.route("")
class Products(Resource):

    def get(self):
        products = product_service.get_all_products()
        return {
            "data": products_schema.dump(products)
        }

    @admin_required
    def post(self):
        try:
            image_1 = save_image("image_1")
            image_2 = save_image("image_2")
            image_3 = save_image("image_3")
            name = request.form['name']
            description = request.form['description']
            price = request.form["price"]
            category_id = request.form["category_id"]
            category = category_service.find_category_by_id(category_id)
            if not category:
                return {
                    "message": "Category doesnot exist",
                    "success": False
                }, 404
            data = {
                "name": name,
                "image_1":image_1,
                "image_2":image_2,
                "image_3":image_3,
                "description": description,
                "price": price,
                "category_id": category_id
            }

            product = product_service.create_product(data)
            return {
                "data": product_schema.dump(product),
                "message": "Product created successfully",
                "success": True
            }
        except BadRequestKeyError as e:
            return {
                "message": str(e) or "Missing some files check if files contain image_1 image_2 or image_3"
            }, 500

        except Exception:
            return {
                "message": "Unable to complete request"
            }, 500        


@api.route("/<product_id>")
class Product(Resource):

    def get(self, product_id):
        product = product_service.find_product_by_id(product_id)
        if not product:
            return {
                "message": "Product Not Found",
                "success": False
            }, 404
        _json = product.serialze() 
        return {
            "data": _json
        }

    @admin_required
    @api.expect(ProductDto.product_update, validate=True)
    def put(self, product_id):
        product = product_service.find_product_by_id(product_id)
        if not product:
            return {
                "message": "Product Not Found",
                "success": False
            }, 404

        if not request.files or request.form:
            return {
            "message": "Please provide on value for update",
            "success": False
            }, 400

        data = {}
        if request.files:
            if "image_1" in request.files:
                data["image_1"] = save_image("image_1")

            if "image_2" in request.files:
                data["image_2"] = save_image("image_2")  

            if "image_3" in request.files:
                data["image_3"] = save_image("image_3") 

        if request.form:

            if "name" in request.form:
                data.name = request.form['name']      
            
            if "description" in request.form:
                data.description = request.form["description"]

            if "price" in request.form:
                data.price = request.form["price"]    

            if "category_id" in request.form:
                category_id = request.form["category_id"]
                category = category_service.find_category_by_id(category_id)
                if not category:
                    return {
                        "message": "Category not Found",
                        "success": False
                    }, 404
                data.category_id = category_id 

        product_service.update_product(product, data)

        return {"message": "Product updated successfully",
                "success": True }

    @admin_required
    def delete(self, product_id):
        product = product_service.find_product_by_id(product_id)
        if not product:
            return {
                "message": "Product Not Found",
                "success": False
            }, 404

        product_service.delete_product(product)

        return {
            "message": "Product Deleted Successfully",
            "success": True
        }