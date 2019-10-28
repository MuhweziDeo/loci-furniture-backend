from json import dumps
from flask import request
from ..models.user import User
from ..services.user_service import get_user_by_email



def get_logged_in_user(*args, **kwargs):
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
            return user["data"]
        except Exception as e:
            return {
            	"success": False,
            	"message": str(e) or "Server Error"
            }

    
