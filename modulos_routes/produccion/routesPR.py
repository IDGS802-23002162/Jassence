
from flask import flash, render_template, request, redirect, abort
from models import (
    OrdenProduccion, Receta, db, ProduccionTemporal,
    Usuario, ProductoTerminado, DetalleReceta, MateriaPrima, Presentacion, Venta, DireccionEntrega
)
from . import produccion_bp
from datetime import datetime
from sqlalchemy import text, desc, func
from modulos_routes.auditoria.utils import registrar_log, generar_resumen_consumo_produccion, generar_detalle_entrada_producto
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

    recetas_activas = Receta.query.filter(Receta.activo == True).all()

    return render_template(
        'modulos_front/produccion/solicitudes.html',
        solicitudes=solicitudes,
        recetas=recetas_activas, 
        presentaciones=Presentacion.query.all()
    )

# REGISTRAR SOLICITUD ---------------------------------

@produccion_bp.route('/produccion/solicitudes/crear', methods=['POST'])
def registrar_solicitud():
    try:
        fecha = datetime.strptime(request.form.get('fecha'), "%Y-%m-%d")
        cantidad = int(request.form.get('cantidad', 0))

        # Validación: cantidad mínima 1
        if cantidad < 1:
            flash("La cantidad debe ser mayor a 0", "error")
            return redirect('/produccion/solicitudes')

        db.session.execute(
            text("CALL sp_crear_solicitud(:receta, :presentacion, :cantidad, :user, :fecha)"),
            {
                "receta": int(request.form.get('id_producto')),
                "presentacion": int(request.form.get('id_presentacion')),
                "cantidad": cantidad,
                "user": current_user.id,
                "fecha": fecha
            }
        )

        db.session.commit()
        flash("Solicitud registrada", "success")

    except Exception as e:
        db.session.rollback()
        print("ERROR REAL >>>", e)
        flash("Error", "error")

    return redirect('/produccion/solicitudes')

# CANCELAR SOLICITUD ---------------------------------

@produccion_bp.route('/produccion/solicitudes/cancelar/<int:id>', methods=['POST'])
def cancelar_solicitud(id):

    try:
        db.session.execute(
            text("CALL sp_cancelar_solicitud(:id)"),
            {"id": id}
        )
        db.session.commit()

        flash("Solicitud cancelada correctamente", "success")

    except Exception as e:
        db.session.rollback()
        print(e)
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
    try:
        # 1. ¡Aquí está la corrección! Agregamos @mensaje al final del CALL
        db.session.execute(
            text("CALL sp_crear_orden(:solicitud, :user, @mensaje)"),
            {
                "solicitud": int(request.form.get('id_solicitud')),
                "user": current_user.id
            }
        )
        
        resultado = db.session.execute(text("SELECT @mensaje")).scalar()
        
        if resultado == 'EXITO':
            db.session.commit()
            flash("¡Orden de producción generada correctamente!", "produccion_success")
        else:
            db.session.rollback()
            flash(f"{resultado}", "produccion_error")

    except Exception as e:
        db.session.rollback()
        print(f"Error técnico al crear orden: {str(e)}")
        flash("Ocurrió un error inesperado al procesar la solicitud.", "produccion_error")

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
                    cantidad_producida = o.cantidad_producir or 0  # <--- evitar None
                    ml = o.producto_terminado.presentacion.mililitros if o.producto_terminado else 0
                    cantidad_usada = (detalle.porcentaje / 100) * (cantidad_producida * ml)

                    stock_real = materia.cantidad_disponible - (materia.stock_apartado or 0)

                    if stock_real < cantidad_usada:
                        o.puede_iniciar = False
                        o.mensaje_stock = f"Falta {materia.nombre}"
                        break

    return render_template(
        'modulos_front/produccion/seguimiento_sin_iniciar.html',
        ordenes=ordenes
    )

# CANCELAR ORDEN ---------------------------------

@produccion_bp.route('/produccion/ordenes/cancelar/<int:id>', methods=['POST'])
@roles_accepted('admin','produccion') 
def cancelar_orden(id):
    try:
        orden = OrdenProduccion.query.get_or_404(id)

        if orden.estado == "terminado":
            flash("No puedes cancelar una orden terminada", "error")
            return redirect('/produccion/seguimiento/sin-iniciar')

        db.session.execute(
            text("CALL sp_cancelar_orden(:id)"),
            {"id": id}
        )

        db.session.commit()

        flash("Orden cancelada correctamente", "success")

    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash("Error al cancelar la orden", "error")

    return redirect('/produccion/seguimiento/sin-iniciar')

# INICIAR PRODUCCIÓN ---------------------------------------


@produccion_bp.route('/produccion/ordenes/iniciar/<int:id>', methods=['POST'])
def iniciar(id):
    try:
        # 👇 VALIDACIÓN AQUÍ
        estado_actual = db.session.execute(
            text("SELECT estado FROM ordenes_produccion WHERE id = :id"),
            {"id": id}
        ).scalar()

        if estado_actual != "pendiente":
            flash("La orden ya fue iniciada o no es válida", "error")
            return redirect('/produccion/seguimiento/sin-iniciar')

        # 👇 TU SP
        db.session.execute(
            text("CALL sp_iniciar_produccion(:id)"),
            {"id": id}
        )

        db.session.commit()
        flash("Producción iniciada correctamente", "success")

    except Exception as e:
        db.session.rollback()
        print(e)
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
def finalizar(id):
    orden = OrdenProduccion.query.get_or_404(id)

    try:
        resumen_mp = generar_resumen_consumo_produccion(orden)
        nombre_receta = orden.receta.nombre_perfume if orden.receta else "Desconocido"
        cantidad_producida = orden.cantidad_producir or 0

        db.session.execute(
            text("CALL sp_finalizar_produccion(:id)"),
            {"id": id}
        )

        # LOG 1: SALIDA de Materia Prima (Se hace siempre)
        registrar_log(
            accion="SALIDA",
            tabla="materias_primas",
            registro_id=id, 
            detalle=f"Consumo por Orden #{id} ({cantidad_producida}x {nombre_receta}): [ {resumen_mp} ]"
        )

        # LOG 2: ENTRADA de Producto Terminado (EXCEPTO si tiene venta_id)
        if not orden.venta_id:
            detalle_entrada = generar_detalle_entrada_producto(orden)
            
            registrar_log(
                accion="ENTRADA",
                tabla="productos_terminados",
                registro_id=orden.producto_terminado_id if orden.producto_terminado else id,
                detalle=detalle_entrada
            )
        db.session.commit()

        flash("Producción finalizada", "success")

    except Exception as e:
        db.session.rollback()
        print(e)
        flash("Error", "error")

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

        # NUEVO: Inyectar el estado de la venta 
        if o.venta_id:
            venta = Venta.query.get(o.venta_id)
            o.estado_venta = venta.estado_pedido if venta else None
        else:
            o.estado_venta = None

    return render_template(
        'modulos_front/produccion/seguimiento_F.html',
        ordenes=ordenes
    )

@produccion_bp.route('/produccion/orden/<int:orden_id>/guia')
@roles_accepted('admin','produccion') 
def imprimir_guia(orden_id):
    orden = OrdenProduccion.query.get_or_404(orden_id)
    if not orden.venta_id:
        abort(400, description="Esta orden no está asociada a una venta online.")
        
    venta = Venta.query.get(orden.venta_id)
    direccion = DireccionEntrega.query.get(venta.direccion_envio_id)
    
    return render_template('modulos_front/produccion/guia_envio.html', orden=orden, venta=venta, direccion=direccion)

# =========================================
# ENVIAR PEDIDO (VENTAS ONLINE)
# =========================================
@produccion_bp.route('/produccion/enviar_pedido/<int:venta_id>', methods=['POST'])
@roles_accepted('admin','produccion') 
def enviar_pedido(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    
    # 1. Validar si hay órdenes de producción sin terminar
    ordenes_pendientes = OrdenProduccion.query.filter(
        OrdenProduccion.venta_id == venta_id,
        OrdenProduccion.estado.in_(['pendiente', 'en_proceso'])
    ).count()

    # 2. NUEVO: Validar si hay solicitudes temporales que aún no se convierten en orden
    solicitudes_pendientes = ProduccionTemporal.query.filter(
        ProduccionTemporal.venta_id == venta_id,
        ProduccionTemporal.estatus == 'pendiente'
    ).count()

    # 3. Evaluamos ambas condiciones
    if ordenes_pendientes > 0 or solicitudes_pendientes > 0:
        flash("No se puede enviar. Hay productos de esta venta en cola de solicitudes o en producción.", "error")
        return redirect(request.referrer)

    # 4. Si pasa la validación y no está enviado ya, ejecutamos el proceso
    if venta.estado_pedido != 'Enviado':
        try:
            # Llamamos al Stored Procedure para descontar stock comprometido y cambiar estado
            db.session.execute(
                text("CALL sp_enviar_pedido(:id)"),
                {"id": venta_id}
            )
            db.session.commit()
            flash("El pedido ha sido marcado como enviado exitosamente.", "success")
            
        except Exception as e:
            db.session.rollback()
            flash("Ocurrió un error inesperado al procesar el envío en la base de datos.", "error")
            print(f"Error al enviar pedido: {e}")
            
    return redirect(request.referrer)