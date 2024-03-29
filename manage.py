import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main import create_app, db
from app import blueprint

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
from app.main.models.user import User
from app.main.models.products import Product
from app.main.models.category import Category
from app.main.models.cart import Cart 

@manager.command
def run():
    app.run()


@manager.command
def test():
    """ Run tests """
    tests = unittest.TestLoader().discover('app/tests', pattern='tests*.py')
    result = unittest.TestRunner(verbose=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
