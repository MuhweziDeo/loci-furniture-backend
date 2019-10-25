from ..models.user import User
from ..services.user_service import get_user_by_email
from functools import wraps
from flask import request


def login_required(f):
    wraps(f)

    def decorated(*args, **kwargs):
        try:
            authorization_header = request.headers.get('Authorization')
            if not authorization_header:
                return {
                           "message": "Unauthorized access",
                           "success": False
                       }, 401
            user = User.decode_auth_token(authorization_header)
            if not user['data']:
                return {
                           "message": user,
                           "success": False
                       }, 403
            return f(*args, **kwargs)
        except Exception as e:
            return e

    return decorated


def admin_required(f):
    wraps(f)

    def decorated(*args, **kwargs):
        try:
            authorization_header = request.headers.get('Authorization')
            if not authorization_header:
                return {
                           "message": "Unauthorized access",
                           "success": False
                       }, 401
            payload = User.decode_auth_token(authorization_header)
            if not payload['data']:
                return {
                           "message": payload,
                           "success": False
                       }, 403
            user = get_user_by_email(payload['data']['email'])
            if not user:
                return {
                           "message": "User not found",
                           "success": False
                       }, 404
            if not user.admin:
                return {
                           "message": "Permission Denied",
                           "success": False
                       }, 401
            return f(*args, **kwargs)
        except Exception as e:
            return e

    return decorated
