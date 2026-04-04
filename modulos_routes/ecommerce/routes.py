
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import extract, func
from models import db, Receta, ProductoTerminado, Carrito, CarritoItem, Venta, DetalleVenta, OrdenProduccion, DetalleReceta, MateriaPrima

ecommerce_bp=Blueprint('ecommerce',__name__)


def tiene_materia_prima_suficiente(producto, cantidad=1):
    detalles = DetalleReceta.query.filter_by(receta_id=producto.receta_id).all()
    if not detalles:
        return False

    ml = producto.presentacion.mililitros

    for det in detalles:
        materia = MateriaPrima.query.get(det.materia_prima_id)
        requerido = (det.porcentaje / 100) * ml * cantidad

        if not materia or materia.cantidad_disponible < requerido:
            return False

    return True


@ecommerce_bp.route("/", methods=["GET", "POST"])
def ecommerce():
    recetas = Receta.query.all()
    nuevas = recetas[-4:] if len(recetas) >= 4 else recetas

    vendidos = db.session.query(Receta)\
        .join(ProductoTerminado)\
        .join(DetalleVenta)\
        .group_by(Receta.id)\
        .order_by(func.sum(DetalleVenta.cantidad).desc())\
        .limit(4).all()
    
    if not vendidos:
        vendidos = recetas[:4] if len(recetas) >= 4 else recetas

    for receta in recetas:
        for producto in receta.productos_terminados:
            if tiene_materia_prima_suficiente(producto):
                producto.tipo_envio = "Envío rápido"
            else:
                producto.tipo_envio = "Envío en 10-15 días"
    
    return render_template("modulos_front/ecommerce/ecommerce.html", recetas=recetas,nuevas=nuevas,vendidos=vendidos)


@ecommerce_bp.route("/agregar_carrito", methods=["POST"])
def agregar_carrito():
    cliente_id = 1  # SIMULACIÓN: Asumimos que el cliente con ID 1 inició sesión
    producto_id = request.form.get('producto_id')
    
    if not producto_id:
        return redirect(url_for('ecommerce.ecommerce'))

    carrito = Carrito.query.filter_by(cliente_id=cliente_id).first()
    
    if not carrito:
        carrito = Carrito(cliente_id=cliente_id)
        db.session.add(carrito)
        db.session.commit() # Lo guardamos para que genere un ID

    item_existente = CarritoItem.query.filter_by(carrito_id=carrito.id, producto_terminado_id=producto_id).first()
    
    if item_existente:
        item_existente.cantidad += 1
    else:
        nuevo_item = CarritoItem(
            carrito_id=carrito.id, 
            producto_terminado_id=producto_id, 
            cantidad=1
        )
        db.session.add(nuevo_item)
    
    db.session.commit()
    # Aquí podríamos poner un flash('Producto agregado al carrito'), pero por ahora solo recargamos
    return jsonify({"success": True})


# --- INYECTOR GLOBAL PARA EL CARRITO ---
@ecommerce_bp.context_processor
def inyectar_carrito_global():
    cliente_id = 1 # Seguimos con nuestro cliente de prueba
    carrito = Carrito.query.filter_by(cliente_id=cliente_id).first()
    
    cantidad_total = 0
    subtotal_carrito = 0
    
    if carrito and carrito.items:
        cantidad_total = sum(item.cantidad for item in carrito.items)
        for item in carrito.items:
            if item.producto_terminado:
                subtotal_carrito += (item.cantidad * item.producto_terminado.precio_venta)
                
    return dict(carrito_global=carrito, cantidad_total=cantidad_total, subtotal_carrito=subtotal_carrito)

# --- RUTA PARA MODIFICAR EL CARRITO (Sumar, Restar, Eliminar) ---
@ecommerce_bp.route("/modificar_carrito", methods=["POST"])
def modificar_carrito():
    item_id = request.form.get('item_id')
    accion = request.form.get('accion')
    
    item = CarritoItem.query.get(item_id)
    
    if item:
        if accion == 'sumar':
            item.cantidad += 1
        elif accion == 'restar':
            item.cantidad -= 1
            if item.cantidad <= 0:
                db.session.delete(item)
        elif accion == 'eliminar':
            db.session.delete(item)
            
        db.session.commit()
        
    # request.referrer nos regresa exactamente a la página donde estábamos (tienda o carrito)
    return redirect(request.referrer or url_for('ecommerce.ecommerce'))

@ecommerce_bp.route("/pagar", methods=["GET", "POST"])
def pagar():
    cliente_id = 1
    carrito = Carrito.query.filter_by(cliente_id=cliente_id).first()
    
    subtotal = 0
    if carrito and carrito.items:
        for item in carrito.items:
            if item.producto_terminado:
                subtotal += (item.cantidad * item.producto_terminado.precio_venta)
    
    iva = subtotal * 0.16
    total = subtotal + iva

    if request.method == "POST":
        if not carrito or not carrito.items:
            return redirect(url_for('ecommerce.ecommerce'))
        
        metodo = request.form.get('metodo_pago', 'Tarjeta Online')

        requiere_produccion_lenta = False

        # 1. Crear venta
        nueva_venta = Venta(
            cliente_id=cliente_id,
            canal_venta='Online',
            estado_pedido='Procesando',  # temporal
            total_venta=total,
            metodo_pago_fisico=metodo
        )
        db.session.add(nueva_venta)
        db.session.flush()  # para obtener el ID

        # 2. Procesar cada item del carrito
        for item in carrito.items:
            prod = item.producto_terminado

            # 🔹 Crear detalle de venta
            det = DetalleVenta(
                venta_id=nueva_venta.id,
                producto_terminado_id=prod.id,
                cantidad=item.cantidad,
                precio_unitario=prod.precio_venta
            )
            db.session.add(det)

            # 🔹 Validar materia prima
            hay_materia = tiene_materia_prima_suficiente(prod, item.cantidad)

            if not hay_materia:
                requiere_produccion_lenta = True

            # 🔹 Crear orden de producción SIEMPRE
            orden = OrdenProduccion(
                receta_id=prod.receta.id,
                venta_id=nueva_venta.id,
                producto_terminado_id=prod.id,
                cantidad_producir=item.cantidad,
                estado = 'pendiente_mp' if not hay_materia else 'lista_para_producir'
            )
            db.session.add(orden)

            # 🔹 Limpiar carrito
            db.session.delete(item)

        # 3. Definir estado final de la venta
        if requiere_produccion_lenta:
            nueva_venta.estado_pedido = 'Pagado - Producción Pendiente (10-15 días)'
        else:
            nueva_venta.estado_pedido = 'Pagado - En Producción (Envío rápido)'

        db.session.commit()

        return redirect(url_for('ecommerce.ticket_e', id=nueva_venta.id))

    return render_template(
        "modulos_front/ecommerce/pago.html",
        carrito=carrito,
        subtotal=subtotal,
        iva=iva,
        total=total
    )

# NUEVA RUTA PARA EL TICKET ONLINE
@ecommerce_bp.route("/ticket_e/<int:id>")
def ticket_e(id):
    venta = Venta.query.get_or_404(id)
    return render_template("modulos_front/ecommerce/ticket_e.html", venta=venta)


    
@ecommerce_bp.route("/nosotros")
def nosotros():

    return render_template("modulos_front/ecommerce/nosotros.html")

@ecommerce_bp.route("/sucursales")
def sucursales():
    # Redirige directamente a una vista general de León, Guanajuato en Google Maps
    url_google_maps = "https://www.google.com/maps/search/León,+Guanajuato"
    
    return redirect(url_google_maps)