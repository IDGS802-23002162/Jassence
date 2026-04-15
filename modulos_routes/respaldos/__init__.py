from flask import Blueprint

respaldos_bp = Blueprint(
    'respaldos',
    __name__,
    template_folder='templates'

)

from . import routesR