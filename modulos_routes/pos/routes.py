from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Receta, ProductoTerminado, MermaInventario, DetalleVenta, Venta
import json
from flask_security import current_user, roles_accepted

pos_bp = Blueprint('pos', __name__)

@pos_bp.route('/pos', methods=['GET'])
@roles_accepted('admin','ventas') 
def pos():
    recetas = Receta.query.filter(Receta.productos_terminados.any()).all()
    return render_template('modulos_front/pos/pos.html', recetas=recetas, titulo="Venta Local")
    

@pos_bp.route('/ticket_pos', methods=['POST', 'GET'])
def ticket_pos():
    if request.method == 'POST':
        datos_carrito_str = request.form.get('datos_carrito')
        metodo_pago = request.form.get('metodo_pago')

        if not datos_carrito_str or datos_carrito_str == '[]':
            flash('El carrito está vacío. Agrega productos antes de cobrar.', 'error')
            return redirect(url_for('pos.pos'))

        try:
            carrito = json.loads(datos_carrito_str)
            total_venta = sum(item['subtotal'] for item in carrito)

            # 3. Creamos la cabecera de la Venta
            nueva_venta = Venta(
                usuario_id=current_user.id, # En el futuro aquí irá current_user.id
                canal_venta='Mostrador',
                estado_pedido='Entregado', # Como es venta física, se entrega al instante
                total_venta=total_venta,
                metodo_pago_fisico=metodo_pago
            )
            db.session.add(nueva_venta)
            db.session.flush() 

            # 4. Procesamos cada perfume del carrito
            for item in carrito:
                producto_id = int(item['productoId'])
                cantidad_vendida = int(item['cantidad'])
                precio_unitario = float(item['precio'])

                producto = ProductoTerminado.query.get(producto_id)
                
                if producto and producto.stock_disponible_venta >= cantidad_vendida:
                    producto.stock_disponible_venta -= cantidad_vendida

                    detalle = DetalleVenta(
                        venta_id=nueva_venta.id,
                        producto_terminado_id=producto.id,
                        cantidad=cantidad_vendida,
                        precio_unitario=precio_unitario
                    )
                    db.session.add(detalle)
                else:
                    db.session.rollback()
                    flash(f'Error: Stock insuficiente para {item["nombre"]}.', 'error')
                    return redirect(url_for('pos.pos'))

            db.session.commit()
            
            return render_template('modulos_front/pos/ticket_pos.html', venta=nueva_venta)
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la venta: {str(e)}', 'error')
            return redirect(url_for('pos.pos'))
            
    # Si alguien intenta entrar a /ticket directo escribiendo la URL (GET)
    flash('Debes realizar una venta para ver un ticket.', 'error')
    return redirect(url_for('pos.pos'))


@pos_bp.route('/registrar_merma_pos', methods=['POST'])
@roles_accepted('admin','ventas') 
def registrar_merma_pos():
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad'))
    motivo = request.form.get('motivo')
    descripcion = request.form.get('descripcion')

    producto = ProductoTerminado.query.get_or_404(producto_id)
    if producto.stock_disponible_venta >= cantidad:
        try:
            # 1. Restamos del inventario físico
            producto.stock_disponible_venta -= cantidad

            # 2. Registramos la evidencia en la tabla MermaInventario
            nueva_merma = MermaInventario(
                tipo_item='producto_terminado',
                item_id=producto.id,
                etapa='ventas_mostrador', 
                usuario_id=current_user.id, # O usar current_user.id si ya tienes login
                cantidad_perdida=cantidad,
                unidad_medida='unidades',
                motivo=motivo,
                descripcion=descripcion
            )
            
            db.session.add(nueva_merma)
            db.session.commit()
            
            flash('Incidente registrado. El stock ha sido actualizado.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar la merma en la base de datos.', 'error')
    else:
        flash('Error: La cantidad reportada supera el stock físico disponible.', 'error')

    return redirect(url_for('pos.pos'))



@pos_bp.route('/historial_V')
@roles_accepted('admin','ventas') 
def historial_V():
    ventas_pos = Venta.query.filter_by(canal_venta='Mostrador').order_by(Venta.fecha.desc()).all()
    return render_template('modulos_front/pos/historial_V.html', ventas=ventas_pos, titulo="Historial de Ventas")


@pos_bp.route('/detalle_V/<int:id>')
@roles_accepted('admin','ventas') 
def detalle_V(id):
    venta = Venta.query.get_or_404(id)
    return render_template('modulos_front/pos/detalle_V.html', venta=venta, titulo="Detalle de Venta")
