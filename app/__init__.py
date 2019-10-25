from flask_restplus import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_ns
from .main.controllers.category_controller import api as category_ns
from .main.controllers.product_controller import api as product_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint,
          title='LOCI FURNITURE',
          version='1.0',
          description='Loci furniture backend api'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(category_ns, path='/category')
api.add_namespace(product_ns, path='/product')
