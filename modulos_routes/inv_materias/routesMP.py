# Archivo: modulos_routes/inv_materias/routesMP.py

from . import invMP_bp
from flask import render_template, request, redirect, url_for
from models import LogAuditoria, db, MermaInventario, MateriaPrima

# ==========================================
# GENERADO DE LOGS DE AUDITORÍA
# ==========================================

def crear_log(accion, tabla, registro_id, detalle, usuario_id=None):
    log = LogAuditoria(
        usuario_id=usuario_id,  # si no hay login, queda None
        accion=accion,
        tabla_afectada=tabla,
        registro_id=registro_id,
        detalle=detalle
    )
    db.session.add(log)

# ==========================================
# MÓDULO: INVENTARIO DE MATERIAS PRIMAS
# ==========================================

@invMP_bp.route('/materias-primas/inventario')
def inventario():
    materias = MateriaPrima.query.all()
    return render_template(
        'modulos_front/inv_materias/inv_MP.html',
        materias=materias 
    )


@invMP_bp.route('/materias-primas/inventario/detalle/<int:id>')
def detalle_MP(id):
    materia = MateriaPrima.query.get_or_404(id)

    return render_template(
        'modulos_front/inv_materias/detalle_MP.html',
        materia=materia  
    )


@invMP_bp.route('/materias-primas/inventario/mermar/<int:id>', methods=['POST'])
def mermar_MP(id):
    materia = MateriaPrima.query.get_or_404(id)

    cantidad = float(request.form.get('cantidad_perdida'))

    if cantidad > materia.cantidad_disponible:
        cantidad = materia.cantidad_disponible

    materia.cantidad_disponible -= cantidad

    nueva_merma = MermaInventario(
        tipo_item="materia_prima",
        item_id=id,
        etapa=request.form.get('etapa'),
        cantidad_perdida=cantidad,
        unidad_medida=request.form.get('unidad_medida'),
        motivo=request.form.get('motivo'),
        descripcion=request.form.get('descripcion')
    )

    db.session.add(nueva_merma)

    crear_log(
    "UPDATE",
    "materias_primas",
    id,
    f"Merma de {cantidad} {materia.unidad_medida} a {materia.nombre}",
    usuario_id=None 
)

    db.session.commit()

    return redirect(url_for('inv_materias.inventario'))


@invMP_bp.route('/materias-primas/Inventario/delete/<int:id>', methods=['POST'])
def eliminar_MP(id):
    materia = MateriaPrima.query.get_or_404(id)

    nombre = materia.nombre 

    db.session.delete(materia)

    crear_log(
        "DELETE",
        "materias_primas",
        id,
        f"Se eliminó la materia prima {nombre}",
        usuario_id=None  # aquí marcas que es el “Sistema”
    )

    db
    db.session.commit()

    return redirect(url_for('inv_materias.inventario'))


# ==========================================
# SUBMÓDULO: MERMAS
# ==========================================

@invMP_bp.route('/materias-primas/mermas')
def mermas():
    mermas = MermaInventario.query.all()

    return render_template(
        'modulos_front/inv_materias/merma_MP.html',
        mermas=mermas
    )


@invMP_bp.route('/materias-primas/mermas/registrar', methods=['GET', 'POST'])
def registrar_merma_mp():

    if request.method == 'POST':
        item_id = request.form.get('item_id')

        if not item_id:
            return "Error: selecciona un insumo"

        materia = MateriaPrima.query.get_or_404(item_id)

        cantidad = float(request.form.get('cantidad_perdida'))

        if materia.cantidad_disponible < cantidad:
            return "Error: no hay suficiente stock"

        materia.cantidad_disponible -= cantidad

        nueva_merma = MermaInventario(
            tipo_item=request.form.get('tipo_item'),
            item_id=materia.id,
            etapa=request.form.get('etapa'),
            cantidad_perdida=cantidad,
            unidad_medida=materia.unidad_medida,
            motivo=request.form.get('motivo'),
            descripcion=request.form.get('descripcion'),
            orden_produccion_id=request.form.get('orden_produccion_id') or None
        )

        crear_log(
            "UPDATE",
            "materias_primas",
            materia.id,
            f"Merma de {cantidad} {materia.unidad_medida} a {materia.nombre}",
            usuario_id=None
        )

        db.session.add(nueva_merma)
        db.session.commit()

        return redirect(url_for('inv_materias.mermas'))

    materias = MateriaPrima.query.all()

    return render_template(
        'modulos_front/inv_materias/registrar_merma_mp.html',
        materias=materias
    )

@invMP_bp.route('/materias-primas/mermas/detalle/<int:id>')
def detalle_merma(id):
    merma = MermaInventario.query.get_or_404(id)

    return render_template(
        'modulos_front/inv_materias/detalle_merma_mp.html',
        merma=merma
    )


# ==========================================
# SUBMÓDULO: HISTORIAL
# ==========================================

@invMP_bp.route('/materias-primas/historial')
def historial():
    historial = LogAuditoria.query\
        .filter_by(tabla_afectada="materias_primas")\
        .order_by(LogAuditoria.fecha.desc())\
        .all()

    return render_template(
        'modulos_front/inv_materias/historial_MP.html',
        historial=historial
    )

@invMP_bp.route('/materias-primas/historial/detalle/<int:id>')
def detalle_historial(id):
    historial = LogAuditoria.query.get_or_404(id)
    return render_template(
        'modulos_front/inv_materias/detalles_H.html',
        historial=historial
    )