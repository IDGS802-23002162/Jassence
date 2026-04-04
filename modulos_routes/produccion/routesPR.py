from flask import flash, render_template, request, redirect
from models import (
    OrdenProduccion, Receta, db, ProduccionTemporal,
    Usuario, ProductoTerminado, DetalleReceta, MateriaPrima
)
from . import produccion_bp
from datetime import datetime


# =========================================
# SOLICITUDES DE PRODUCCIÓN
# =========================================

@produccion_bp.route('/produccion/solicitudes', methods=['GET'])
def index_solicitudes():
    solicitudes = ProduccionTemporal.query.order_by(ProduccionTemporal.fecha.desc()).all()

    # Asignar el nombre de la receta
    recetas_dict = {r.id: r.nombre_perfume for r in Receta.query.all()}
    for s in solicitudes:
        s.receta_nombre = recetas_dict.get(s.receta_id, "Desconocido")
        s.estado = "pendiente"  # Siempre pendiente mientras no haya orden

    return render_template(
        'modulos_front/produccion/solicitudes.html',
        solicitudes=solicitudes,
        recetas=Receta.query.all()
    )


@produccion_bp.route('/produccion/solicitudes/crear', methods=['POST'])
def registrar_solicitud():
    producto_id = request.form.get('id_producto')
    cantidad = request.form.get('cantidad')
    fecha_solicitada = request.form.get('fecha')

    if not (producto_id and cantidad and fecha_solicitada):
        flash("Todos los campos son obligatorios", "error")
        return redirect('/produccion/solicitudes')

    try:
        fecha = datetime.strptime(fecha_solicitada, "%Y-%m-%d")
    except ValueError:
        flash("Formato de fecha inválido", "error")
        return redirect('/produccion/solicitudes')

    nueva = ProduccionTemporal(
        receta_id=int(producto_id),
        cantidad=int(cantidad),
        creado_por=1,
        fecha=fecha
    )

    try:
        db.session.add(nueva)
        db.session.commit()
        flash("Solicitud registrada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al registrar solicitud", "error")

    return redirect('/produccion/solicitudes')


# =========================================
# ORDENES DE PRODUCCIÓN
# =========================================

@produccion_bp.route('/produccion/ordenes', methods=['GET'])
def index_ordenes():
    solicitudes = ProduccionTemporal.query.order_by(ProduccionTemporal.fecha.desc()).all()
    ordenes = OrdenProduccion.query.filter(OrdenProduccion.estado.in_(["pendiente", "en_proceso"])).all()
    responsables = Usuario.query.filter_by(estado=True).all()
    recetas_dict = {r.id: r.nombre_perfume for r in Receta.query.all()}

    for s in solicitudes:
        s.receta_nombre = recetas_dict.get(s.receta_id, "Desconocido")
        # Estado de solicitud se mantiene pendiente, la orden tendrá su propio estado
        s.estado = "pendiente"

    return render_template(
        'modulos_front/produccion/ordenes.html',
        solicitudes=solicitudes,
        responsables=responsables,
        ordenes=ordenes
    )

# =========================================
# CREAR ORDEN
# =========================================

@produccion_bp.route('/produccion/ordenes/crear', methods=['POST'])
def crear_orden():
    solicitud_id = request.form.get('id_solicitud')
    cantidad = request.form.get('cantidad_producir')
    responsable_id = request.form.get('responsable_id')

    if not (solicitud_id and cantidad):
        flash("Todos los campos son obligatorios", "error")
        return redirect('/produccion/ordenes')

    solicitud = ProduccionTemporal.query.get(int(solicitud_id))
    if not solicitud:
        flash("Solicitud no encontrada", "error")
        return redirect('/produccion/ordenes')

    producto = ProductoTerminado.query.filter_by(receta_id=solicitud.receta_id).first()
    if not producto:
        flash("No existe producto terminado para esta receta", "error")
        return redirect('/produccion/ordenes')

    # Ahora la orden se crea con estado "en_proceso" directamente
    nueva = OrdenProduccion(
        receta_id=solicitud.receta_id,
        producto_terminado_id=producto.id,
        cantidad_producir=int(cantidad),
        responsable_id=int(responsable_id) if responsable_id else None,
        fecha_solicitud=datetime.utcnow(),
        estado="pendiente"  # ✅ aquí comienza la producción
    )

    try:
        db.session.add(nueva)
        db.session.commit()
        # Eliminar solicitud temporal
        db.session.delete(solicitud)
        db.session.commit()
        flash("Orden creada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al crear orden", "error")

    return redirect('/produccion/ordenes')

# =========================================
# SEGUIMIENTO
# =========================================

@produccion_bp.route('/produccion/seguimiento')
def index_seguimiento():
    return redirect('/produccion/seguimiento/sin-iniciar')


# =========================================
# SIN INICIAR
# =========================================

@produccion_bp.route('/produccion/seguimiento/sin-iniciar')
def seguimiento_sin_iniciar():
    ordenes = OrdenProduccion.query.filter_by(estado="pendiente").all()

    recetas = {r.id: r.nombre_perfume for r in Receta.query.all()}
    usuarios = {u.id: u.nombre for u in Usuario.query.all()}

    for o in ordenes:
        o.receta_nombre = recetas.get(o.receta_id, "Desconocido")
        o.responsable_nombre = usuarios.get(o.responsable_id, "Sin asignar")

    return render_template(
        'modulos_front/produccion/seguimiento_sin_iniciar.html',
        ordenes=ordenes
    )


# =========================================
# PARA FINALIZAR
# =========================================

@produccion_bp.route('/produccion/seguimiento/para-finalizar')
def seguimiento_para_finalizar():
    ordenes = OrdenProduccion.query.filter_by(estado="en_proceso").all()

    recetas = {r.id: r.nombre_perfume for r in Receta.query.all()}
    usuarios = {u.id: u.nombre for u in Usuario.query.all()}

    for o in ordenes:
        o.receta_nombre = recetas.get(o.receta_id, "Desconocido")
        o.responsable_nombre = usuarios.get(o.responsable_id, "Sin asignar")

    return render_template(
        'modulos_front/produccion/seguimiento_para_finalizar.html',
        ordenes=ordenes
    )


# =========================================
# INICIAR PRODUCCIÓN
# =========================================

@produccion_bp.route('/produccion/ordenes/iniciar/<int:id>', methods=['POST'])
def iniciar_produccion(id):
    orden = OrdenProduccion.query.get_or_404(id)

    if orden.estado != "pendiente":
        flash("La orden no se puede iniciar", "error")
        return redirect('/produccion/seguimiento/sin-iniciar')

    orden.estado = "en_proceso"
    orden.fecha_inicio = datetime.utcnow()

    try:
        db.session.commit()
        flash("Producción iniciada", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al iniciar producción", "error")

    return redirect('/produccion/seguimiento/sin-iniciar')


# =========================================
# FINALIZAR PRODUCCIÓN
# =========================================
@produccion_bp.route('/produccion/ordenes/finalizar/<int:id>', methods=['POST'])
def finalizar_produccion(id):
    # Obtener la orden
    orden = OrdenProduccion.query.get_or_404(id)

    if orden.estado != "en_proceso":
        flash("La orden no se puede finalizar", "error")
        return redirect('/produccion/seguimiento/para-finalizar')

    # Obtener la receta
    receta = Receta.query.get(orden.receta_id)
    if not receta:
        flash("Receta no encontrada", "error")
        return redirect('/produccion/seguimiento/para-finalizar')

    # Validar y restar materias primas según porcentaje y cantidad a producir
    for detalle in receta.detalles:
        materia = MateriaPrima.query.get(detalle.materia_prima_id)
        if materia:
            cantidad_usada = (detalle.porcentaje / 100) * orden.cantidad_producir
            if materia.cantidad_disponible < cantidad_usada:
                flash(f"No hay suficiente {materia.nombre} para producir la orden", "error")
                return redirect('/produccion/seguimiento/para-finalizar')
            materia.cantidad_disponible -= cantidad_usada

    # Revisar si existe el producto terminado
    producto = ProductoTerminado.query.filter_by(
        receta_id=orden.receta_id,
        presentacion_id=orden.producto_terminado_id  # si usas presentación, cambiar según corresponda
    ).first()

    if producto:
        # Si existe, sumar stock
        if producto.stock_disponible_venta is None:
            producto.stock_disponible_venta = 0
        producto.stock_disponible_venta += orden.cantidad_producir
    else:
        # Si no existe, crear nuevo producto terminado
        producto = ProductoTerminado(
            receta_id=orden.receta_id,
            presentacion_id=orden.producto_terminado_id,  # actualizar si tienes otro campo
            stock_disponible_venta=orden.cantidad_producir,
            stock_comprometido=0,
            stock_minimo=0,
            precio_venta=0,  # o el que corresponda
            estado="activo"
        )
        db.session.add(producto)

    # Finalizar la orden
    orden.estado = "terminado"
    orden.fecha_fin = datetime.utcnow()

    # Guardar todos los cambios
    try:
        db.session.commit()
        flash("Producción finalizada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al finalizar producción", "error")

    return redirect('/produccion/seguimiento/para-finalizar')