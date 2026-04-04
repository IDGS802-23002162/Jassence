
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import extract, func
from models import db, Receta, ProductoTerminado, Carrito, CarritoItem, Venta, DetalleVenta, OrdenProduccion, DetalleReceta, MateriaPrima, Cliente, DireccionEntrega, MetodoPagoCliente
import re
from datetime import datetime

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
        
        # 1. Recuperamos los textos exactos que vienen del HTML
        metodo_val = request.form.get('metodo_pago') 
        direccion_id = request.form.get('direccion_id') # En el HTML le pusimos name="direccion_id"
        
        # 2. Variables iniciales
        id_tarjeta = None
        metodo_fisico = None

        # 3. Lógica inteligente de asignación
        if metodo_val and metodo_val.startswith('tarjeta_'):
            # Si el valor es "tarjeta_5", lo separamos por el guion bajo y nos quedamos con el "5"
            id_tarjeta = int(metodo_val.split('_')[1])
        else:
            # Si eligió "paypal", el ID de tarjeta queda nulo y guardamos "paypal" como físico
            metodo_fisico = metodo_val

        requiere_produccion_lenta = False

        # 4. Crear venta con los datos correctos
        nueva_venta = Venta(
            cliente_id=cliente_id,
            canal_venta='Online',
            estado_pedido='Procesando',  # temporal
            total_venta=total,
            direccion_envio_id=direccion_id,
            metodo_pago_id=id_tarjeta,
            metodo_pago_fisico=metodo_fisico
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

    direcciones = DireccionEntrega.query.filter_by(cliente_id=cliente_id, estado=True).all()
    metodos_pago = MetodoPagoCliente.query.filter_by(cliente_id=cliente_id, estado=True).all()
    dir_principal = next((d for d in direcciones if d.es_principal), direcciones[0] if direcciones else None)

    return render_template(
        "modulos_front/ecommerce/pago.html",
        carrito=carrito,
        subtotal=subtotal,
        iva=iva,
        total=total,
        direcciones=direcciones,
        metodos_pago=metodos_pago,
        dir_principal=dir_principal
    )

@ecommerce_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    cliente_id = 1  # Simulación de usuario logueado
    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        flash("Cliente no encontrado", "error")
        return redirect(url_for('ecommerce.ecommerce'))

    if request.method == "POST":
        # 1. Actualizamos los datos en el objeto Cliente
        cliente.nombre = request.form.get("nombre")
        cliente.apellidos = request.form.get("apellidos")
        cliente.telefono = request.form.get("telefono")

        # 2. Actualizamos los datos en el objeto Usuario relacionado
        if cliente.usuario:
            cliente.usuario.email = request.form.get("correo")
            # Sincronizamos nombre/teléfono en Usuario si así lo requiere tu lógica
            cliente.usuario.nombre = request.form.get("nombre")
            cliente.usuario.apellidos = request.form.get("apellidos")
            cliente.usuario.telefono = request.form.get("telefono")

        try:
            # 3. Este commit guarda los cambios de AMBOS objetos (Cliente y Usuario)
            db.session.commit()
            flash("Datos actualizados correctamente", "success")
        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar los datos", "error")
            print(f"Error en DB: {e}")

        return redirect(url_for('ecommerce.perfil'))

    # Carga de datos para el GET
    direcciones = DireccionEntrega.query.filter_by(cliente_id=cliente_id, estado=True).all()
    metodos = MetodoPagoCliente.query.filter_by(cliente_id=cliente_id, estado=True).all()

    return render_template(
        "modulos_front/ecommerce/perfil.html",
        cliente=cliente,
        direcciones=direcciones,
        metodos=metodos
    )

@ecommerce_bp.route("/direcciones", methods=["POST"])   
def modal_direcciones():
    cliente_id = 1 # Considera obtener esto de current_user después
    
    es_predeterminada = True if request.form.get("es_principal") else False

    if es_predeterminada:
        DireccionEntrega.query.filter_by(cliente_id=cliente_id, es_principal=True).update({"es_principal": False})

    nueva = DireccionEntrega(
        cliente_id=cliente_id,
        nombre_receptor=request.form.get("nombre"),
        telefono_contacto=request.form.get("telefono"),
        calle_numero=request.form.get("calle"),
        colonia=request.form.get("colonia"),
        ciudad=request.form.get("ciudad"),
        estado_provincia=request.form.get("estado"),
        codigo_postal=request.form.get("cp"),
        referencias=request.form.get("referencias"),
        es_principal=es_predeterminada,
        estado=True
    )

    try:
        db.session.add(nueva)
        db.session.commit()
        flash("Dirección guardada exitosamente", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error al guardar la dirección", "error")
        print(f"Error: {e}")

    return redirect(url_for('ecommerce.perfil'))

@ecommerce_bp.route("/direcciones/eliminar/<int:id>", methods=["POST"])
def eliminar_direccion(id):
    direccion = DireccionEntrega.query.get_or_404(id)
    cliente_id = direccion.cliente_id
    direccion.estado = False
    
    # Si eliminamos la principal, buscamos otra para suplirla
    if direccion.es_principal:
        direccion.es_principal = False # Ya no es principal porque se "borró"
        otra = DireccionEntrega.query.filter_by(cliente_id=cliente_id, estado=True).filter(DireccionEntrega.id != id).first()
        if otra:
            otra.es_principal = True
            
    db.session.commit()
    flash("Dirección eliminada correctamente", "success")
    return redirect(url_for('ecommerce.perfil'))

@ecommerce_bp.route("/direcciones/editar/<int:id>", methods=["POST"])
def editar_direccion(id):
    direccion = DireccionEntrega.query.get_or_404(id)
    cliente_id = 1 # Reemplazar por current_user.id
    
    es_predeterminada = True if request.form.get("es_principal") else False

    if es_predeterminada:
        # Quitamos principal a las otras
        DireccionEntrega.query.filter_by(cliente_id=cliente_id, es_principal=True).update({"es_principal": False})

    # Actualizamos campos
    direccion.nombre_receptor = request.form.get("nombre")
    direccion.telefono_contacto = request.form.get("telefono")
    direccion.calle_numero = request.form.get("calle")
    direccion.colonia = request.form.get("colonia")
    direccion.ciudad = request.form.get("ciudad")
    direccion.estado_provincia = request.form.get("estado")
    direccion.codigo_postal = request.form.get("cp")
    direccion.referencias = request.form.get("referencias")
    direccion.es_principal = es_predeterminada

    db.session.commit()
    flash("Dirección actualizada", "success")
    return redirect(url_for('ecommerce.perfil'))

# VALIDACIONES PARA TIPOS DE PAGO

def limpiar_numero(numero):
    return re.sub(r"\D", "", numero)

def detectar_marca(numero):
    if numero.startswith("4"):
        return "VISA"
    elif re.match(r"^5[1-5]", numero):
        return "MASTERCARD"
    elif re.match(r"^3[47]", numero):
        return "AMEX"
    return "OTRA"

def validar_luhn(numero):
    suma = 0
    reverso = numero[::-1]

    for i, d in enumerate(reverso):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        suma += n

    return suma % 10 == 0

# ----------------------------------------------------

@ecommerce_bp.route("/tipos_pago", methods=["POST"])
def modal_tipos_pago():
    cliente_id = 1

    numero_raw = request.form.get("numero")
    exp_raw = request.form.get("exp")

    if not numero_raw or not exp_raw:
        flash("Datos incompletos", "error")
        return redirect(url_for('ecommerce.perfil'))

    numero = limpiar_numero(numero_raw)
    if not validar_luhn(numero):
        flash("Tarjeta inválida", "error")
        return redirect(url_for('ecommerce.perfil'))
    marca = detectar_marca(numero)
    try:
        fecha = datetime.strptime(exp_raw, "%m/%y")
        mes = fecha.month
        anio = fecha.year
    except:
        flash("Fecha inválida", "error")
        return redirect(url_for('ecommerce.perfil'))

    # FAKE STRIPE IDS
    stripe_customer_id = f"cus_test_{cliente_id}"
    stripe_payment_method_id = f"pm_test_{numero[-4:]}"

    es_primera = not MetodoPagoCliente.query.filter_by(cliente_id=cliente_id, estado=True).first()

    nueva = MetodoPagoCliente(
        cliente_id=cliente_id,

        stripe_customer_id=stripe_customer_id,
        stripe_payment_method_id=stripe_payment_method_id,

        tipo_tarjeta=marca,
        ultimos_4=numero[-4:],
        exp_mes=mes,
        exp_anio=anio, 

        es_principal=es_primera,
        estado=True
    )

    db.session.add(nueva)
    db.session.commit()

    flash("Tarjeta guardada correctamente", "success")
    return redirect(url_for('ecommerce.perfil'))

@ecommerce_bp.route("/metodo_pago/eliminar/<int:id>", methods=["POST"])
def eliminar_metodo_pago(id):
    metodo = MetodoPagoCliente.query.get_or_404(id)
    cliente_id = metodo.cliente_id
    
    metodo.estado = False
    
    if metodo.es_principal:
        metodo.es_principal = False
        otro = MetodoPagoCliente.query.filter_by(cliente_id=cliente_id, estado=True).filter(MetodoPagoCliente.id != id).first()
        if otro:
            otro.es_principal = True

    db.session.commit()
    flash("Método de pago eliminado", "success")
    return redirect(url_for('ecommerce.perfil'))

@ecommerce_bp.route("/pedidos")
def pedidos():
    cliente_id = 1  # luego será current_user.id

    ventas = Venta.query\
        .filter_by(cliente_id=cliente_id)\
        .order_by(Venta.id.desc())\
        .all()

    return render_template(
        "modulos_front/ecommerce/pedidos.html",
        ventas=ventas)

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