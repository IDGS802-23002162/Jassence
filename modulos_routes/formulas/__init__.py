from flask import Blueprint

formulas_bp = Blueprint(
    'formulas',
    __name__,
    template_folder='templates'
)

from . import routesFOR
