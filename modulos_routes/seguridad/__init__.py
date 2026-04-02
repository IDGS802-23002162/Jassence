from flask import Blueprint

seguridad = Blueprint(
    'seguridad',
    __name__,
    template_folder='templates'

)

from . import routes