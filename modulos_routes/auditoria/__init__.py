from flask import Blueprint

auditorias = Blueprint(
    'auditorias',
    __name__,
    template_folder='templates'

)

from . import routes