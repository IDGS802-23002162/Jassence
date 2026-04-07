from flask import flash, render_template, request, redirect
from models import (
    OrdenProduccion, Receta, db, ProduccionTemporal,
    Usuario, ProductoTerminado, DetalleReceta, MateriaPrima, Presentacion
)
from . import produccion_bp
from datetime import datetime
from flask_security import current_user, roles_accepted

# =========================================
# SOLICITUDES DE PRODUCCIÓN
# =========================================

@produccion_bp.route('/produccion/solicitudes', methods=['GET'])
def index_solicitudes():
    solicitudes = ProduccionTemporal.query.order_by(ProduccionTemporal.fecha.desc()).all()

    recetas_dict = {r.id: r.nombre_perfume for r in Receta.query.all()}
    presentaciones = {p.id: p.nombre for p in Presentacion.query.all()} 

    for s in solicitudes:
        s.receta_nombre = recetas_dict.get(s.receta_id, "Desconocido")
        s.presentacion_nombre = presentaciones.get(s.presentacion_id, "N/A")  
        s.estado = "pendiente"

    return render_template(
        'modulos_front/produccion/solicitudes.html',
        solicitudes=solicitudes,
        recetas=Receta.query.all(),
        presentaciones=Presentacion.query.all()
    )

# REGISTRAR SOLICITUD ---------------------------------

@produccion_bp.route('/produccion/solicitudes/crear', methods=['POST'])
@roles_accepted('admin','produccion') 
def registrar_solicitud():
    producto_id = request.form.get('id_producto')
    presentacion_id = request.form.get('id_presentacion')  # 👈 NUEVO
    cantidad = request.form.get('cantidad')
    fecha_solicitada = request.form.get('fecha')

    if not (producto_id and cantidad and fecha_solicitada and presentacion_id):
        flash("Todos los campos son obligatorios", "error")
        return redirect('/produccion/solicitudes')

    try:
        fecha = datetime.strptime(fecha_solicitada, "%Y-%m-%d")
    except ValueError:
        flash("Formato de fecha inválido", "error")
        return redirect('/produccion/solicitudes')

    nueva = ProduccionTemporal(
        receta_id=int(producto_id),
        presentacion_id=int(presentacion_id),  # 👈 CLAVE
        cantidad=int(cantidad),
        creado_por=current_user.id,
        fecha=fecha,
        estatus="pendiente"
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

# CANCELAR SOLICITUD ---------------------------------

@produccion_bp.route('/produccion/solicitudes/cancelar/<int:id>', methods=['POST'])
@roles_accepted('admin','produccion') 
def cancelar_solicitud(id):
    solicitud = ProduccionTemporal.query.get_or_404(id)

    try:
        db.session.delete(solicitud)
        db.session.commit()
        flash("Solicitud cancelada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al cancelar la solicitud", "error")

    return redirect('/produccion/solicitudes')

# =========================================
# ORDENES DE PRODUCCIÓN
# =========================================

@produccion_bp.route('/produccion/ordenes', methods=['GET'])
@roles_accepted('admin','produccion') 
def index_ordenes():
    solicitudes = ProduccionTemporal.query.order_by(ProduccionTemporal.fecha.desc()).all()
    ordenes = OrdenProduccion.query.filter(OrdenProduccion.estado.in_(["pendiente", "en_proceso"])).all()
    responsables = Usuario.query.filter_by(active=True).all()

    recetas_dict = {r.id: r.nombre_perfume for r in Receta.query.all()}

    for s in solicitudes:
        s.receta_nombre = recetas_dict.get(s.receta_id, "Desconocido")
        s.presentacion_nombre = f"{s.presentacion.nombre} - {s.presentacion.mililitros} ml" if s.presentacion else "N/A"
        s.estado = "pendiente"

    return render_template(
        'modulos_front/produccion/ordenes.html',
        solicitudes=solicitudes,
        responsables=responsables,
        ordenes=ordenes
    )

# CREAR ORDEN ---------------------------------

@produccion_bp.route('/produccion/ordenes/crear', methods=['POST'])
@roles_accepted('admin','produccion') 
def crear_orden():
    solicitud_id = request.form.get('id_solicitud')

    if not solicitud_id:
        flash("Selecciona una solicitud", "error")
        return redirect('/produccion/ordenes')

    solicitud = ProduccionTemporal.query.get(int(solicitud_id))

    if not solicitud:
        flash("Solicitud no encontrada", "error")
        return redirect('/produccion/ordenes')

    producto = ProductoTerminado.query.filter_by(
        receta_id=solicitud.receta_id,
        presentacion_id=solicitud.presentacion_id
    ).first()

    if not producto:
        producto = ProductoTerminado(
            receta_id=solicitud.receta_id,
            presentacion_id=solicitud.presentacion_id,
            stock_disponible_venta=0,
            stock_comprometido=0,
            stock_minimo=0,
            precio_venta=0,
            estado="activo"
        )
        db.session.add(producto)
        db.session.flush()

    nueva = OrdenProduccion(
        receta_id=solicitud.receta_id,
        producto_terminado_id=producto.id,
        cantidad_producir=solicitud.cantidad,
        responsable_id=current_user.id,  
        fecha_solicitud=datetime.now(),  
        estado="pendiente"
    )

    try:
        db.session.add(nueva)
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
@roles_accepted('admin','produccion') 
def index_seguimiento():
    return redirect('/produccion/seguimiento/sin-iniciar')


# =========================================
# ORDENES PENDIENTES 
# =========================================

@produccion_bp.route('/produccion/seguimiento/sin-iniciar')
@roles_accepted('admin','produccion') 
def seguimiento_sin_iniciar():
    ordenes = OrdenProduccion.query.filter_by(estado="pendiente").all()

    for o in ordenes:
        o.receta_nombre = o.receta.nombre_perfume if o.receta else "Desconocido"
        o.responsable_nombre = o.responsable.nombre if o.responsable else "Sin asignar"
        o.responsable_apellidos = o.responsable.apellidos if o.responsable else "Sin asignar"

        if o.producto_terminado and o.producto_terminado.presentacion:
            o.presentacion_nombre = o.producto_terminado.presentacion.nombre
            o.presentacion_mililitros = o.producto_terminado.presentacion.mililitros
        else:
            o.presentacion_nombre = "N/A"
            o.presentacion_mililitros = ""

        o.puede_iniciar = True
        o.mensaje_stock = ""

        receta = o.receta

        if receta:
            for detalle in receta.detalles:
                materia = MateriaPrima.query.get(detalle.materia_prima_id)

                if materia:
                    cantidad_usada = (detalle.porcentaje / 100) * o.cantidad_producir

                    if materia.cantidad_disponible < cantidad_usada:
                        o.puede_iniciar = False
                        o.mensaje_stock = f"Falta {materia.nombre}"
                        break

    return render_template(
        'modulos_front/produccion/seguimiento_sin_iniciar.html',
        ordenes=ordenes
    )

@produccion_bp.route('/produccion/ordenes/cancelar/<int:id>', methods=['POST'])
@roles_accepted('admin','produccion') 
def cancelar_orden(id):
    orden = OrdenProduccion.query.get_or_404(id)

    if orden.estado != "pendiente":
        flash("Solo se pueden cancelar órdenes pendientes", "error")
        return redirect('/produccion/seguimiento/sin-iniciar')

    try:
        orden.estado = "cancelado"

        db.session.commit()
        flash("Orden cancelada correctamente", "success")

    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al cancelar la orden", "error")

    return redirect('/produccion/seguimiento/sin-iniciar')

# INICIAR PRODUCCIÓN ---------------------------------------


@produccion_bp.route('/produccion/ordenes/iniciar/<int:id>', methods=['POST'])
@roles_accepted('admin','produccion') 
def iniciar_produccion(id):
    orden = OrdenProduccion.query.get_or_404(id)

    if orden.estado != "pendiente":
        flash("La orden no se puede iniciar", "error")
        return redirect('/produccion/seguimiento/sin-iniciar')

    receta = Receta.query.get(orden.receta_id)

    if not receta:
        flash("Receta no encontrada", "error")
        return redirect('/produccion/seguimiento/sin-iniciar')

    # 🔥 VALIDAR MATERIA PRIMA
    for detalle in receta.detalles:
        materia = MateriaPrima.query.get(detalle.materia_prima_id)

        if materia:
            cantidad_usada = (detalle.porcentaje / 100) * orden.cantidad_producir

            if materia.cantidad_disponible < cantidad_usada:
                flash(f"No hay suficiente {materia.nombre}", "error")
                return redirect('/produccion/seguimiento/sin-iniciar')

    orden.estado = "en_proceso"
    orden.fecha_inicio = datetime.now()

    try:
        db.session.commit()
        flash("Producción iniciada", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al iniciar producción", "error")

    return redirect('/produccion/seguimiento/sin-iniciar')


# =========================================
# ORDENES EN PROCESO 
# =========================================

@produccion_bp.route('/produccion/seguimiento/para-finalizar')
@roles_accepted('admin','produccion') 
def seguimiento_para_finalizar():
    ordenes = OrdenProduccion.query.filter_by(estado="en_proceso").all()

    for o in ordenes:
        o.receta_nombre = o.receta.nombre_perfume if o.receta else "Desconocido"
        o.responsable_nombre = o.responsable.nombre if o.responsable else "Sin asignar"
        o.responsable_apellidos = o.responsable.apellidos if o.responsable else "Sin asignar"


        if o.producto_terminado and o.producto_terminado.presentacion:
            o.presentacion_nombre = o.producto_terminado.presentacion.nombre
            o.presentacion_mililitros = o.producto_terminado.presentacion.mililitros
        else:
            o.presentacion_nombre = "N/A"
            o.presentacion_mililitros = ""

    return render_template(
        'modulos_front/produccion/seguimiento_para_finalizar.html',
        ordenes=ordenes
    )   


# FINALIZAR PRODUCCIÓN ---------------------------------------

@produccion_bp.route('/produccion/ordenes/finalizar/<int:id>', methods=['POST'])
@roles_accepted('admin','produccion') 
def finalizar_produccion(id):

    orden = OrdenProduccion.query.get_or_404(id)

    if orden.estado != "en_proceso":
        flash("La orden no se puede finalizar", "error")
        return redirect('/produccion/seguimiento/para-finalizar')

    producto = ProductoTerminado.query.get(orden.producto_terminado_id)

    if not producto:
        flash("Producto no encontrado", "error")
        return redirect('/produccion/seguimiento/para-finalizar')

    receta = Receta.query.get(orden.receta_id)

    if not receta:
        flash("Receta no encontrada", "error")
        return redirect('/produccion/seguimiento/para-finalizar')

    for detalle in receta.detalles:
        materia = MateriaPrima.query.get(detalle.materia_prima_id)

        if materia:
            cantidad_usada = (detalle.porcentaje / 100) * orden.cantidad_producir

            if materia.cantidad_disponible < cantidad_usada:
                flash(f"No hay suficiente {materia.nombre}", "error")
                return redirect('/produccion/seguimiento/para-finalizar')

            materia.cantidad_disponible -= cantidad_usada

    if not producto.stock_disponible_venta:
        producto.stock_disponible_venta = 0

    producto.stock_disponible_venta += orden.cantidad_producir

    orden.estado = "terminado"
    orden.fecha_fin = datetime.now()  

    try:
        db.session.commit()
        flash("Producción finalizada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al finalizar producción", "error")

    return redirect('/produccion/seguimiento/para-finalizar')


# =========================================
# ORDENES FINALIZADAS 
# =========================================

@produccion_bp.route('/produccion/seguimiento_F', methods=['GET'])
@roles_accepted('admin','produccion') 
def seguimiento_F():
    ordenes = OrdenProduccion.query.filter(
        OrdenProduccion.estado.in_(["terminado", "cancelado"])
    ).order_by(OrdenProduccion.fecha_fin.desc()).all()

    for o in ordenes:
        o.receta_nombre = o.receta.nombre_perfume if o.receta else "Desconocido"
        o.responsable_nombre = o.responsable.nombre if o.responsable else "Sin asignar"
        o.responsable_apellidos = o.responsable.apellidos if o.responsable else ""

        if o.producto_terminado and o.producto_terminado.presentacion:
            o.presentacion_nombre = o.producto_terminado.presentacion.nombre
            o.presentacion_mililitros = o.producto_terminado.presentacion.mililitros
        else:
            o.presentacion_nombre = "N/A"
            o.presentacion_mililitros = ""

        if o.estado == "terminado":
            o.estado_color = "bg-green-500 text-green-50"
        elif o.estado == "cancelado":
            o.estado_color = "bg-red-500 text-red-50"
        else:
            o.estado_color = "bg-gray-500 text-gray-50"

    return render_template(
        'modulos_front/produccion/seguimiento_F.html',
        ordenes=ordenes
    )