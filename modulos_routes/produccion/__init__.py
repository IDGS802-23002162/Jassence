from flask import Blueprint, render_template, redirect

# 1. Definimos el Blueprint para Producción
produccion_bp = Blueprint('produccion', __name__)

@produccion_bp.route('/produccion/solicitudes', methods=['GET'])
def index_solicitudes():
    # Asegúrate de guardar el HTML en esta ruta más adelante
    return render_template('modulos_front/produccion/solicitudes.html')

@produccion_bp.route('/produccion/ordenes', methods=['GET'])
def index_ordenes():
    return render_template('modulos_front/produccion/ordenes.html')

# Ruta general de seguimiento redirige a "Sin iniciar" por defecto
@produccion_bp.route('/produccion/seguimiento', methods=['GET'])
def index_seguimiento():
    return redirect('/produccion/seguimiento/sin-iniciar')

@produccion_bp.route('/produccion/seguimiento/sin-iniciar', methods=['GET'])
def seguimiento_sin_iniciar():
    return render_template('modulos_front/produccion/seguimiento_sin_iniciar.html')

@produccion_bp.route('/produccion/seguimiento/para-finalizar', methods=['GET'])
def seguimiento_para_finalizar():
    return render_template('modulos_front/produccion/seguimiento_para_finalizar.html')