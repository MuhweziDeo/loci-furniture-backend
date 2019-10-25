from flask import request, jsonify
from flask_restplus import Resource
from ..services import category_service
from ..utils.dto import CategoryDto
from ..utils.decorator import admin_required

api = CategoryDto.api
_category = CategoryDto.category


@api.route("")
class Categories(Resource):

    @api.marshal_list_with(_category, envelope='data')
    def get(self):
        categories = category_service.find_all_categories()
        return categories

    @admin_required
    @api.expect(_category, validate=True)
    def post(self):
        try:
            data = request.json
            category = category_service.find_category_by_name(data['name'])
            if category:
                return {
                           "message": "Category with name {} exists".format(data['name']),
                           "success": False
                       }, 409
            new_category = category_service.create_category(data)
            category_json = new_category.serialize()
            return jsonify({
                "message": "Category successfully created",
                "data": category_json,
                "success": True
            })
        except Exception as e:
            return {
                       "message": str(e) or "Couldn't complete request",
                       "success": False
                   }, 500


@api.route("/<category_id>")
class Category(Resource):

    @api.doc("category object")
    def get(self, category_id):
        category = category_service.find_category_by_id(category_id)
        if not category:
            return {
                       "message": "Category not found",
                       "success": False
                   }, 404
        _json = category.serialize()
        return {
            "data": _json
        }

    @api.expect(_category, validate=True)
    def put(self, category_id):
        category = category_service.find_category_by_id(category_id)
        if not category:
            return {
                       "message": "Category not found",
                       "success": False
                   }, 404
        updated = category_service.update_category(category, request.json['name'])

        return {
            "message": "Successfully updated",
            "data": updated.serialize()
        }

    @api.doc("Delete category")
    def delete(self, category_id):
        category = category_service.find_category_by_id(category_id)
        if not category:
            return {
                       "message": "Category not found",
                       "success": False
                   }, 404

        deleted = category_service.delete_category(category)
        return {
            "message": "Deleted successfully",
            "success": True,
            "data": deleted.serialize()
        }
