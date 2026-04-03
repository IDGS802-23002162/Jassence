
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import extract, func
from models import db, Receta, ProductoTerminado, Carrito, CarritoItem, Venta, DetalleVenta
ecommerce_bp=Blueprint('ecommerce',__name__)


@ecommerce_bp.route("/", methods=["GET", "POST"])
def ecommerce():
    recetas = Receta.query.filter(Receta.productos_terminados.any(ProductoTerminado.stock_disponible_venta > 0)).all()
    nuevas = recetas[-4:] if len(recetas) >= 4 else recetas

    vendidos = db.session.query(Receta)\
        .join(ProductoTerminado)\
        .join(DetalleVenta)\
        .group_by(Receta.id)\
        .order_by(func.sum(DetalleVenta.cantidad).desc())\
        .limit(4).all()
    
    if not vendidos:
        vendidos = recetas[:4] if len(recetas) >= 4 else recetas
    
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
    return redirect(url_for('ecommerce.ecommerce'))


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

        # 1. Creamos la venta
        nueva_venta = Venta(
            cliente_id=cliente_id,
            canal_venta='Online',
            estado_pedido='Pagado - Preparando Envío',
            total_venta=total,
            metodo_pago_fisico=metodo
        )
        db.session.add(nueva_venta)
        db.session.flush()

        # 2. Pasamos los items a Detalles y descontamos stock
        for item in carrito.items:
            prod = item.producto_terminado
            if prod.stock_disponible_venta >= item.cantidad:
                prod.stock_disponible_venta -= item.cantidad
                
                det = DetalleVenta(
                    venta_id=nueva_venta.id, 
                    producto_terminado_id=prod.id, 
                    cantidad=item.cantidad, 
                    precio_unitario=prod.precio_venta
                )
                db.session.add(det)
            
            # 3. Borramos el item del carrito
            db.session.delete(item)

        db.session.commit()
        return redirect(url_for('ecommerce.ticket_e', id=nueva_venta.id))

    return render_template("modulos_front/ecommerce/pago.html", carrito=carrito, subtotal=subtotal, iva=iva, total=total)

# NUEVA RUTA PARA EL TICKET ONLINE
@ecommerce_bp.route("/ticket_e/<int:id>")
def ticket_e(id):
    venta = Venta.query.get_or_404(id)
    return render_template("modulos_front/ecommerce/ticket_e.html", venta=venta)


@ecommerce_bp.route("/ticket", methods=["GET", "POST"])
def ticket():

    return render_template("modulos_front/ecommerce/ticket.html")

    
@ecommerce_bp.route("/nosotros")
def nosotros():

    return render_template("modulos_front/ecommerce/nosotros.html")

@ecommerce_bp.route("/sucursales")
def sucursales():
    # Redirige directamente a una vista general de León, Guanajuato en Google Maps
    url_google_maps = "https://www.google.com/maps/search/León,+Guanajuato"
    
    return redirect(url_google_maps)