from flask import request, jsonify, abort
from flask_restplus import Resource, reqparse
from ..utils.dto import UserDto
from ..services.user_service import create_user, get_user_by_username, get_user_by_email, get_all_users, verify_user, update_password
from ..models.user import User
from ..utils.decorator import login_required, admin_required

api = UserDto.api
_user = UserDto.user
_login = UserDto.login


@api.route('/')
class UserList(Resource):
    @login_required
    @api.doc('user_resource_list')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """ List all users """
        return get_all_users()

    @api.doc('create_user')
    @api.expect(_user, validate=True)
    def post(self):
        """ Register New User """
        data = request.json
        existing_user_by_email = get_user_by_username(data['email'])
        existing_user_by_username = get_user_by_username(data['username'])
        if(existing_user_by_email or existing_user_by_username):
            message = 'Email already taken' if existing_user_by_email else 'Username already taken'
            field = 'email' if existing_user_by_email else 'username'
            return {
                "message": message,
                "field": field,
                "success": False
            }, 409
        user = create_user(data)
        user_json = user.serialize()
        user.send_email_confirmation_email()
        return {
            "data": user_json,
            "message": "Signed Up successfully Please check email to complete registration",
            "success": True
        }
  

@api.route('/login')
class UserLogin(Resource):
    @api.doc('user_login')
    @api.expect(_login, validate=True)
    def post(self):
        """ Login User """
        data = request.json
        email = data['email']
        password = data['password']
        user = get_user_by_email(email)
        if user is None:
            return {
                "message": "User Not Found",
                "field": 'username'
            }, 404
        if user.check_password(password):
            token = user.encode_token()
            return {
                "message": 'Login Success',
                "success": True,
                "data": {
                    "username": user.username,
                    "isAdmin": user.admin,
                    "token": token.decode("utf-8")
                }
            }     
        return {
            "message": "Invalid password",
            "success": False
        }, 401

@api.route('/email-confirmation/<token>')
class UserEmailConfirmation(Resource):
    @api.doc('email_confirmation')
    def put(self, token):
        try:
            user = get_user_by_email(User.decode_auth_token(token)["data"]["email"])
            if user is None:
                return {
                    "success": False,
                    "message": "User not Found"
                }, 404
            if user.isVerified:
                return {
                    "message": "User already verified",
                    "success": False
                }, 400 
            verify_user(user) 
            data = user.serialize()
            token = user.encode_token()   
            return {
                "message": "Email verification completed successfully",
                "data": data,
                "token": token.decode("utf-8")
            }
        except Exception as e:
            print(e)
            return {
                "success": False,
                "message": "Link has expired or is invalid"
            }, 500

@api.route('/password-reset/request/')
class PasswordResetRequest(Resource):
    @api.doc('request_password_reset')
    @api.expect(UserDto.password_reset_request, validate=True)
    def post(self):
        data = request.json
        user = get_user_by_email(data['email'])
        user.send_reset_password_email() if user else None
        return {
            "message": "Password reset link has been sent to your email",
            "success": True
        }     

@api.route('/password-reset/confirm/<token>')
class PasswordResetConfirm(Resource):
    @api.doc('request_password_confirm')
    @api.expect(UserDto.password_reset_confirm, validate=True)
    def put(self, token):
        try:
            payload = User.decode_auth_token(token)
            user = get_user_by_email(payload["data"]["email"])
            if not user:
                return {
                    "message": "User not found",
                    "success": False
                }, 404
            data = request.json
            update_password(user, data['password'])
            return {
                "message": "Password successfully updated",
                "success": True
            } 
        except Exception:
            return {
                "message": "Something went wrong",
                "success": False
            }
            


@api.route('/me')
class Me(Resource):
    @login_required
    @api.doc('me')
    def get(self):
        try:
            payload = User.decode_auth_token(request.headers.get('Authorization'))
            user = get_user_by_email(payload["data"]["email"])
            if not user:
                return {
                    "message": "User not found",
                    "success": False
                }, 404
            data = user.serialize()
            return {
                "data": data
            }    
        except Exception as e:
            return e
        