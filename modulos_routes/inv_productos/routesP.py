from models import db, LogAuditoria, MermaInventario, ProductoTerminado, OrdenProduccion
from . import inventarioP_bp
from flask import render_template, request, redirect, url_for

class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

# ==========================================
# LOG DE AUDITORÍA
# ==========================================

def crear_log(accion, tabla, registro_id, detalle, usuario_id=None):
    log = LogAuditoria(
        usuario_id=usuario_id,
        accion=accion,
        tabla_afectada=tabla,
        registro_id=registro_id,
        detalle=detalle
    )
    db.session.add(log)

# ==========================================
# INVENTARIO PRODUCTOS TERMINADOS
# ==========================================

@inventarioP_bp.route('/inventario_P')
def inventario_P():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    productos = ProductoTerminado.query.all()

    return render_template(
        'modulos_front/inv_productos/inv_P.html',
        current_user=usuario_logueado,
        productos=productos
    )

# ------------------------------------------

@inventarioP_bp.route('/detalle_P/<int:id>')
def detalle_P(id):
    producto = ProductoTerminado.query.get_or_404(id)

    ordenes_stock_fisico = OrdenProduccion.query.filter_by(
        producto_terminado_id=id,
        venta_id=None 
    ).all()

    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/detalle_P.html',
        current_user=usuario_logueado,
        producto=producto,
        ordenes=ordenes_stock_fisico # El HTML solo recibe lo que es para la tienda
    )

# ------------------------------------------

@inventarioP_bp.route('/merma_Pmodel/<int:id>', methods=['POST'])
def merma_Pmodel(id):
    producto = ProductoTerminado.query.get_or_404(id)


    cantidad = int(request.form['cantidad_perdida'])

    if cantidad > producto.stock_disponible_venta:
        cantidad = producto.stock_disponible_venta

    producto.stock_disponible_venta -= cantidad

    nueva_merma = MermaInventario(
        tipo_item='producto_terminado',
        item_id=id,
        etapa=request.form['etapa'],
        cantidad_perdida=cantidad,
        unidad_medida="unidad",  # Ajusta si manejas otra lógica
        motivo=request.form['motivo'],
        descripcion=request.form['descripcion'],
        orden_produccion_id=request.form.get('orden_produccion_id')
    )

    db.session.add(nueva_merma)

    crear_log(
        "UPDATE",
        "productos_terminados",
        id,
        f"Merma registrada: {cantidad} unidades en etapa {request.form['etapa']}",
        usuario_id=None
    )

    db.session.commit()

    return redirect(url_for('inventarioP.inventario_P'))

@inventarioP_bp.route('/ordenes_por_producto/<int:producto_id>')
def ordenes_por_producto(producto_id):
    ordenes = OrdenProduccion.query.filter_by(
        producto_terminado_id=producto_id
    ).all()

    data = [
        {
            "id": o.id,
            "estado": o.estado
        }
        for o in ordenes
    ]

    return {"ordenes": data}

# ------------------------------------------

@inventarioP_bp.route('/eliminar_P/<int:id>', methods=['POST'])
def eliminar_P(id):
    producto = ProductoTerminado.query.get_or_404(id)

    db.session.delete(producto)

    crear_log(
        accion="DELETE",
        tabla="productos_terminados",
        registro_id=id,
        detalle=f"Producto eliminado ID: {id}",
        usuario_id=None
    )

    db.session.commit()

    return redirect(url_for('inventarioP.inventario_P'))

# ==========================================
# MERMAS
# ==========================================

@inventarioP_bp.route('/inventario_PM')
def inventario_PM():
    mermas = MermaInventario.query.all()

    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/inventario_PM.html',
        current_user=usuario_logueado,
        mermas=mermas
    )

# ------------------------------------------

@inventarioP_bp.route('/registrar_PM', methods=['GET', 'POST'])
def registrar_PM():
    if request.method == 'POST':
        item_id = request.form.get('item_id')

        if not item_id:
            return "ID del producto es requerido", 400

        producto = ProductoTerminado.query.get_or_404(item_id)
        cantidad = int(request.form.get('cantidad_perdida'))

        if producto.stock_disponible_venta < cantidad:
            return "Cantidad de merma excede el stock disponible", 400

        producto.stock_disponible_venta -= cantidad

        nueva_merma = MermaInventario(
            tipo_item='producto_terminado',
            item_id=producto.id,
            etapa=request.form.get('etapa'),
            cantidad_perdida=cantidad,
            unidad_medida="unidad",
            motivo=request.form.get('motivo'),
            descripcion=request.form.get('descripcion'),
            orden_produccion_id=request.form.get('orden_produccion_id')
        )

        crear_log(
            "UPDATE",
            "productos_terminados",
            producto.id,
            f"Merma registrada: {cantidad} unidades en etapa {request.form.get('etapa')}",
            usuario_id=None
        )

        db.session.add(nueva_merma)
        db.session.commit()

        return redirect(url_for('inventarioP.inventario_PM'))

    productos = ProductoTerminado.query.all()

    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/registrar_PM.html',
        current_user=usuario_logueado,
        productos=productos
    )

# ------------------------------------------

@inventarioP_bp.route('/detalle_Pmerma/<int:id>')
def detalle_Pmerma(id):
    merma = MermaInventario.query.get_or_404(id)

    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/detalle_Pmerma.html',
        current_user=usuario_logueado,
        merma=merma
    )

# ==========================================
# HISTORIAL
# ==========================================

@inventarioP_bp.route('/historial_P')
def historial_P():
    historial = LogAuditoria.query\
        .filter_by(tabla_afectada='productos_terminados')\
        .order_by(LogAuditoria.fecha.desc())\
        .all()

    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")

    return render_template(
        'modulos_front/inv_productos/historial_P.html',
        current_user=usuario_logueado,
        historial=historial
    )

# ------------------------------------------

@inventarioP_bp.route('/detalle_PH/<int:id>')
def detalle_PH(id):
    historial = LogAuditoria.query.get_or_404(id)

    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")

    return render_template(
        'modulos_front/inv_productos/detalle_PH.html',
        current_user=usuario_logueado,
        historial=historial
    )