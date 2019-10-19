from .. import db, flask_bcrypt, mail
from flask_mail import Message
from flask import render_template, url_for
import jwt
import datetime
from ..utils.send_email import send_email
import os

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    isVerified = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "admin": self.admin,
            "email": self.email,
            "registered_on": str(self.registered_on)
        }

    def encode_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                "data": {
                    "id": self.id,
                    "email": self.email,
                    "username": self.username,
                    "admin": self.admin
                }
            }
            return jwt.encode(
                payload,
                os.getenv("SECRET_KEY", "randomkey"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod 
    def decode_auth_token(auth_token):
            try:
                payload = jwt.decode(auth_token, os.getenv("SECRET_KEY", "randomkey"))
                return payload
            except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'


    def send_email_confirmation_email(self):
        token = self.encode_token()
        activation_url = os.getenv('AUTH_URL', 
        "http://127.0.0.1:5000/api/v1/user/email-confirmation/")
        confirmation_link = str(activation_url) + "{}".format(token.decode('utf-8'))
        print(confirmation_link)
        data = {
            "username": self.username,
            "email": self.email,
            "confirmation_link": confirmation_link
        }
        send_email("Email Confirmation", [self.email], data,"aggrey256@gmail.com", 
        "confirmation_email.html")

    def send_reset_password_email(self):
        token = self.encode_token()
        auth_url = os.getenv('AUTH_URL', 
        "http://127.0.0.1:5000/api/v1/user/password-reset/confirm/")
        reset_password_link = str(auth_url) + "{}".format(token.decode('utf-8'))
        print(reset_password_link)
        data = {
            "username": self.username,
            "email": self.email,
            "confirmation_link": reset_password_link
        }

        send_email("Password Request Email", [self.email], data,"aggrey256@gmail.com", 
        "password_reset_email.html")

