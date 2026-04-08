# Archivo: modulos_routes/inv_materias/routesMP.py

from . import invMP_bp
from flask import render_template, request, redirect, url_for, flash
from models import LogAuditoria, db, MermaInventario, MateriaPrima
from flask_security import roles_accepted, current_user

# ==========================================
# GENERADO DE LOGS DE AUDITORÍA
# ==========================================

def crear_log(accion, tabla, registro_id, detalle, usuario_id=None):
    log = LogAuditoria(
        usuario_id=current_user.id,
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
@roles_accepted('admin','inventario','produccion')
def inventario():
    # Ahora trae todas las materias primas sin distinguir contenedores
    materias = MateriaPrima.query.all()
    return render_template(
        'modulos_front/inv_materias/inv_MP.html',
        materias=materias 
    )


@invMP_bp.route('/materias-primas/inventario/detalle/<int:id>')
@roles_accepted('admin','inventario','produccion')
def detalle_MP(id):
    materia = MateriaPrima.query.get_or_404(id)
    return render_template(
        'modulos_front/inv_materias/detalle_MP.html',
        materia=materia  
    )


@invMP_bp.route('/materias-primas/inventario/mermar/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario','produccion')
def mermar_MP(id):
    materia = MateriaPrima.query.get_or_404(id)
    
    try:
        cantidad = float(request.form.get('cantidad_perdida', 0))
        
        if cantidad <= 0:
            flash("La cantidad de merma debe ser mayor a cero", "error")
            return redirect(url_for('inv_materias.inventario'))

        if cantidad > materia.cantidad_disponible:
            cantidad = materia.cantidad_disponible

        materia.cantidad_disponible -= cantidad

        nueva_merma = MermaInventario(
            tipo_item="materia_prima",
            item_id=id,
            etapa=request.form.get('etapa'),
            cantidad_perdida=cantidad,
            unidad_medida=materia.unidad_medida, # Usamos la de la materia prima directamente
            motivo=request.form.get('motivo'),
            descripcion=request.form.get('descripcion')
        )

        db.session.add(nueva_merma)

        crear_log(
            "UPDATE",
            "materias_primas",
            id,
            f"Merma registrada: {cantidad} {materia.unidad_medida} de {materia.nombre}"
        )

        db.session.commit()
        flash(f"Merma de {materia.nombre} registrada correctamente", "success")

    except ValueError:
        flash("Error: Ingrese un valor numérico válido", "error")

    return redirect(url_for('inv_materias.inventario'))


@invMP_bp.route('/materias-primas/Inventario/delete/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario','produccion')
def eliminar_MP(id):
    materia = MateriaPrima.query.get_or_404(id)
    nombre = materia.nombre 

    # IMPORTANTE: Antes de borrar, registramos el log
    crear_log(
        "DELETE",
        "materias_primas",
        id,
        f"Se eliminó la materia prima: {nombre}"
    )

    db.session.delete(materia)
    db.session.commit()

    flash(f"Insumo {nombre} eliminado del inventario", "success")
    return redirect(url_for('inv_materias.inventario'))


# ==========================================
# SUBMÓDULO: MERMAS
# ==========================================

@invMP_bp.route('/materias-primas/mermas')
@roles_accepted('admin','inventario','produccion')
def mermas():
    mermas = MermaInventario.query.order_by(MermaInventario.fecha.desc()).all()
    return render_template(
        'modulos_front/inv_materias/merma_MP.html',
        mermas=mermas
    )


@invMP_bp.route('/materias-primas/mermas/registrar', methods=['GET', 'POST'])
@roles_accepted('admin','inventario','produccion')
def registrar_merma_mp():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        if not item_id:
            flash("Error: Selecciona un insumo", "error")
            return redirect(url_for('inv_materias.registrar_merma_mp'))

        materia = MateriaPrima.query.get_or_404(item_id)
        
        try:
            cantidad = float(request.form.get('cantidad_perdida', 0))

            if materia.cantidad_disponible < cantidad:
                flash(f"Error: Stock insuficiente de {materia.nombre}", "error")
                return redirect(url_for('inv_materias.registrar_merma_mp'))

            materia.cantidad_disponible -= cantidad

            nueva_merma = MermaInventario(
                tipo_item="materia_prima",
                item_id=materia.id,
                etapa=request.form.get('etapa'),
                cantidad_perdida=cantidad,
                unidad_medida=materia.unidad_medida,
                motivo=request.form.get('motivo'),
                descripcion=request.form.get('descripcion'),
                orden_produccion_id=request.form.get('orden_produccion_id') or None
            )

            db.session.add(nueva_merma)

            crear_log(
                "UPDATE",
                "materias_primas",
                materia.id,
                f"Merma de {cantidad} {materia.unidad_medida} a {materia.nombre}"
            )

            db.session.commit()
            flash("Merma registrada con éxito", "success")
            return redirect(url_for('inv_materias.mermas'))

        except ValueError:
            flash("Error: La cantidad debe ser un número", "error")

    materias = MateriaPrima.query.all()
    return render_template(
        'modulos_front/inv_materias/registrar_merma_mp.html',
        materias=materias
    )

@invMP_bp.route('/materias-primas/mermas/detalle/<int:id>')
@roles_accepted('admin','inventario','produccion')
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
@roles_accepted('admin','inventario','produccion')
def historial():
    # Filtramos logs específicos de este módulo
    historial = LogAuditoria.query\
        .filter_by(tabla_afectada="materias_primas")\
        .order_by(LogAuditoria.fecha.desc())\
        .all()

    return render_template(
        'modulos_front/inv_materias/historial_MP.html',
        historial=historial
    )

@invMP_bp.route('/materias-primas/historial/detalle/<int:id>')
@roles_accepted('admin','inventario','produccion')
def detalle_historial(id):
    historial = LogAuditoria.query.get_or_404(id)
    return render_template(
        'modulos_front/inv_materias/detalles_H.html',
        historial=historial
    )