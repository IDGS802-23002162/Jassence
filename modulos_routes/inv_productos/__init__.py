from flask import Blueprint

inventarioP_bp = Blueprint(
    'inventarioP',
    __name__,
    template_folder='templates'
)

from . import routesP