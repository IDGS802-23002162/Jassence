from flask import Blueprint

invMP_bp = Blueprint(
    'inv_materias',
    __name__,
    template_folder='templates'
)

from . import routesMP