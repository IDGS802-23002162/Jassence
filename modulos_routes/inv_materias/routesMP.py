# Archivo: modulos_routes/inv_materias/routesMP.py
from . import invMP_bp

from flask import render_template

@invMP_bp.route('/inventarioMP')
def inventario():
    return render_template('modulos_front/inv_materias/inv_MP.html')

@invMP_bp.route('/mermaMP')
def merma():
    return render_template('modulos_front/inv_materias/merma_MP.html')

@invMP_bp.route('/historialMP')
def historial():
    return render_template('modulos_front/inv_materias/historial_MP.html')