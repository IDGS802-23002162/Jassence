from flask import Blueprint

ecommerce = Blueprint(
    'ecommerce',
    __name__,
    template_folder='templates'

)

from . import routes