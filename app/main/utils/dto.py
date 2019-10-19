from flask_restplus import Namespace, fields

class UserDto:
    """DATA TRANSFER OPERATIONS"""
    api = Namespace('user', description='user related options')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

    login = api.model('login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

    password_reset_request = api.model('password_reset_request', {
        'email': fields.String(required=True, description='user email address'),
    })

    password_reset_confirm = api.model('password_reset_request', {
        'password': fields.String(required=True, description='user new password'),
        'password_confirmation': fields.String(required=True, description='user new password'),
    })

