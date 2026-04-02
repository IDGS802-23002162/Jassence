from . import formulas_bp
from flask import render_template, request, redirect, url_for

@formulas_bp.route('/explosion-materiales', methods=['GET'])
def index_formulas():
    return render_template('modulos_front/formulas/formulas.html', titulo="Gestión de Fórmulas")

@formulas_bp.route('/formulas/nueva', methods=['GET'])
def nueva_formula():
    return render_template('modulos_front/formulas/nueva_formula.html')

# (Opcional por ahora) Aquí dejaremos preparada la ruta POST para cuando guardes datos
@formulas_bp.route('/formulas/guardar', methods=['POST'])
def guardar_formula():
    # Aquí irá la lógica de Python y MySQL más adelante
    pass