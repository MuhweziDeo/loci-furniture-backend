from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_uploads import UploadSet, configure_uploads, IMAGES
from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    return app
