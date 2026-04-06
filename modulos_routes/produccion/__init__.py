from flask import Blueprint

# 1. Definimos el Blueprint para Producción
produccion_bp = Blueprint(
    'produccion',
    __name__,
    template_folder='templates'
)

from . import routesPR
