# Archivo: modulos_routes/inv_materias/routesMP.py
from . import invMP_bp
from flask import render_template, request

# ==========================================
# MÓDULO: INVENTARIO DE MATERIAS PRIMAS
# ==========================================

@invMP_bp.route('/materias-primas/inventario')
def inventario():
    return render_template('modulos_front/inv_materias/inv_MP.html')


# ==========================================
# SUBMÓDULO: MERMAS
# ==========================================

@invMP_bp.route('/materias-primas/mermas')
def mermas():
    return render_template('modulos_front/inv_materias/merma_MP.html')

@invMP_bp.route('/materias-primas/mermas/registrar', methods=['GET', 'POST'])
def registrar_merma():
    # Aquí irá tu lógica de POST cuando guardes el formulario
    if request.method == 'POST':
        pass 
    return render_template('modulos_front/inv_materias/registrar_merma_mp.html')

@invMP_bp.route('/materias-primas/mermas/detalle/<int:id>')
def detalle_merma(id):
    # 'id' se recibe de la URL para consultar la base de datos
    return render_template('modulos_front/inv_materias/detalle_merma_mp.html', id=id)


# ==========================================
# SUBMÓDULO: HISTORIAL DE AUDITORÍA
# ==========================================

@invMP_bp.route('/materias-primas/historial')
def historial():
    return render_template('modulos_front/inv_materias/historial_MP.html')

@invMP_bp.route('/materias-primas/historial/detalle/<int:id>')
def detalle_historial(id):
    # 'id' se recibe de la URL para consultar la base de datos
    return render_template('modulos_front/inv_materias/detalles_H.html', id=id)