import uuid
import datetime

from app.main import db
from app.main.models.user import User


def get_all_users():
    return User.query.all()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_user(data):
    user = User(
        public_id=str(uuid.uuid4()),
        email=data['email'].lower(),
        username=data['username'].lower(),
        password=data['password'],
        registered_on=datetime.datetime.utcnow()
    )
    save_changes(user)
    return user


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def verify_user(user):
    user.isVerified = True
    db.session.commit()

def update_password(user, new_password):
    user.password = new_password
    db.session.commit()

