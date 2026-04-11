from models import db, LogAuditoria, MermaInventario, ProductoTerminado, OrdenProduccion, Receta
from . import inventarioP_bp
from flask import render_template, request, redirect, url_for
from flask_security import roles_accepted, current_user
from modulos_routes.auditoria.utils import registrar_log

# ==========================================
# INVENTARIO PRODUCTOS TERMINADOS
# ==========================================


@inventarioP_bp.route('/inventario_P')
@roles_accepted('admin','inventario','produccion')
def inventario_P():
    productos = ProductoTerminado.query\
        .join(Receta)\
        .filter(Receta.activo == True)\
        .all()

    return render_template(
        'modulos_front/inv_productos/inv_P.html',
        productos=productos
    )

# ------------------------------------------

@inventarioP_bp.route('/detalle_P/<int:id>')
@roles_accepted('admin','inventario','produccion')
def detalle_P(id):
    producto = ProductoTerminado.query.get_or_404(id)

    ordenes_stock_fisico = OrdenProduccion.query.filter_by(
        producto_terminado_id=id,
        venta_id=None 
    ).all()

    return render_template(
        'modulos_front/inv_productos/detalle_P.html',
        producto=producto,
        ordenes=ordenes_stock_fisico # El HTML solo recibe lo que es para la tienda
    )

# ------------------------------------------

@inventarioP_bp.route('/merma_Pmodel/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario','produccion')
def merma_Pmodel(id):
    producto = ProductoTerminado.query.get_or_404(id)


    cantidad = int(request.form['cantidad_perdida'])
    motivo = request.form['motivo']

    if cantidad > producto.stock_disponible_venta:
        cantidad = producto.stock_disponible_venta

    producto.stock_disponible_venta -= cantidad

    nueva_merma = MermaInventario(
        tipo_item='producto_terminado',
        item_id=id,
        etapa=request.form['etapa'],
        cantidad_perdida=cantidad,
        unidad_medida="unidad",  # Ajusta si manejas otra lógica
        motivo=motivo,
        descripcion=request.form['descripcion'],
        orden_produccion_id=request.form.get('orden_produccion_id')
    )

    db.session.add(nueva_merma)
    db.session.flush()

    nombre_perfume = producto.receta.nombre_perfume if producto.receta else "Producto Desconocido"
    presentacion = f"{producto.presentacion.nombre} {producto.presentacion.mililitros}ml" if producto.presentacion else ""

    registrar_log(
        accion="MERMA",
        tabla="merma_inventario(PRODUCTO)", 
        registro_id=nueva_merma.id,
        detalle=f"Merma en Almacén: -{cantidad} {nombre_perfume} {presentacion}. Razón: {motivo}"
    )

    db.session.commit()

    return redirect(url_for('inventarioP.inventario_P'))

@inventarioP_bp.route('/ordenes_por_producto/<int:producto_id>')
@roles_accepted('admin','inventario','produccion')
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
@roles_accepted('admin','inventario','produccion')
def eliminar_P(id):
    producto = ProductoTerminado.query.get_or_404(id)

    db.session.delete(producto)

    registrar_log(
        accion="DELETE",
        tabla="productos_terminados",
        registro_id=id,
        detalle=f"Producto eliminado ID: {id}",
    )

    db.session.commit()

    return redirect(url_for('inventarioP.inventario_P'))

# ==========================================
# MERMAS
# ==========================================

@inventarioP_bp.route('/inventario_PM')
@roles_accepted('admin','inventario','produccion')
def inventario_PM():
    mermas = MermaInventario.query.all()

    return render_template(
        'modulos_front/inv_productos/inventario_PM.html',
        mermas=mermas
    )

# ------------------------------------------

@inventarioP_bp.route('/registrar_PM', methods=['GET', 'POST'])
@roles_accepted('admin','inventario','produccion')
def registrar_PM():
    if request.method == 'POST':
        item_id = request.form.get('item_id')

        if not item_id:
            return "ID del producto es requerido", 400

        producto = ProductoTerminado.query.get_or_404(item_id)
        cantidad = int(request.form.get('cantidad_perdida'))
        motivo = request.form.get('motivo')

        if producto.stock_disponible_venta < cantidad:
            return "Cantidad de merma excede el stock disponible", 400

        producto.stock_disponible_venta -= cantidad

        nueva_merma = MermaInventario(
            tipo_item='producto_terminado',
            item_id=producto.id,
            etapa=request.form.get('etapa'),
            cantidad_perdida=cantidad,
            unidad_medida="unidad",
            motivo=motivo,
            descripcion=request.form.get('descripcion'),
            orden_produccion_id=request.form.get('orden_produccion_id')
        )

        db.session.add(nueva_merma)
        db.session.flush()

        nombre_perfume = producto.receta.nombre_perfume if producto.receta else "Producto Desconocido"
        presentacion = f"{producto.presentacion.nombre} {producto.presentacion.mililitros}ml" if producto.presentacion else ""

        registrar_log(
            accion="MERMA",
            tabla="merma_inventario(PRODUCTO)",
            registro_id=nueva_merma.id, # <--- Corregido: antes tenías 'id' que no existía aquí
            detalle=f"Merma en Almacén: -{cantidad} {nombre_perfume} {presentacion}. Razón: {motivo}"
        )
        db.session.commit()

        return redirect(url_for('inventarioP.inventario_PM'))

    productos = ProductoTerminado.query.all()

    return render_template(
        'modulos_front/inv_productos/registrar_PM.html',
        productos=productos
    )

# ------------------------------------------

@inventarioP_bp.route('/detalle_Pmerma/<int:id>')
@roles_accepted('admin','inventario','produccion')
def detalle_Pmerma(id):
    merma = MermaInventario.query.get_or_404(id)

    return render_template(
        'modulos_front/inv_productos/detalle_Pmerma.html',
        merma=merma
    )

# ==========================================
# HISTORIAL
# ==========================================

@inventarioP_bp.route('/historial_P')
@roles_accepted('admin','inventario','produccion')
def historial_P():
    historial = LogAuditoria.query\
        .filter_by(tabla_afectada='productos_terminados')\
        .order_by(LogAuditoria.fecha.desc())\
        .all()


    return render_template(
        'modulos_front/inv_productos/historial_P.html',
        historial=historial
    )

# ------------------------------------------

@inventarioP_bp.route('/detalle_PH/<int:id>')
@roles_accepted('admin','inventario','produccion')
def detalle_PH(id):
    historial = LogAuditoria.query.get_or_404(id)


    return render_template(
        'modulos_front/inv_productos/detalle_PH.html',
        historial=historial
    )