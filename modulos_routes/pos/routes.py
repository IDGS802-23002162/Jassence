from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Receta, ProductoTerminado, MermaInventario, DetalleVenta, Venta, POSSesion, EgresoCaja
import json
from flask_security import current_user, roles_accepted
from modulos_routes.auditoria.utils import registrar_log
pos_bp = Blueprint('pos', __name__)



# ==========================================
# 1. LA PANTALLA DEL POS (Con bloqueo de caja)
# ==========================================
@pos_bp.route('/pos', methods=['GET'])
@roles_accepted('admin','ventas') 
def pos():
    # Buscamos si el usuario actual tiene una caja abierta
    sesion_activa = POSSesion.query.filter_by(usuario_id=current_user.id, estado='abierta').first()
    
    recetas = Receta.query.filter(Receta.productos_terminados.any()).all()
    
    # Mandamos una variable 'caja_abierta' al HTML para saber si bloqueamos la pantalla o no
    return render_template('modulos_front/pos/pos.html', 
                           recetas=recetas, 
                           titulo="Venta Local",
                           caja_abierta=(sesion_activa is not None),
                           sesion_activa=sesion_activa)

# ==========================================
# 2. RUTA PARA ABRIR LA CAJA
# ==========================================
@pos_bp.route('/abrir_caja', methods=['POST'])
@roles_accepted('admin','ventas')
def abrir_caja():
    monto_inicial = float(request.form.get('monto_apertura', 0.0))
    
    # Creamos la nueva sesión
    nueva_sesion = POSSesion(
        usuario_id=current_user.id,
        monto_apertura=monto_inicial,
        estado='abierta'
    )
    db.session.add(nueva_sesion)
    db.session.commit()
    
    flash(f'¡Caja abierta exitosamente con ${monto_inicial}!', 'success')
    return redirect(url_for('pos.pos'))

# ==========================================
# 3. RUTA PARA RETIRAR DINERO (EGRESOS)
# ==========================================
@pos_bp.route('/registrar_egreso', methods=['POST'])
@roles_accepted('admin','ventas')
def registrar_egreso():
    sesion_activa = POSSesion.query.filter_by(usuario_id=current_user.id, estado='abierta').first()
    
    if not sesion_activa:
        flash('No puedes registrar un retiro si la caja está cerrada.', 'error')
        return redirect(url_for('pos.pos'))
        
    monto = float(request.form.get('monto', 0.0))
    motivo = request.form.get('motivo', '')
    
    nuevo_egreso = EgresoCaja(
        sesion_id=sesion_activa.id,
        usuario_id=current_user.id,
        monto=monto,
        motivo=motivo
    )
    
    db.session.add(nuevo_egreso)
    db.session.commit()
    
    flash(f'Retiro de ${monto} registrado por: {motivo}', 'success')
    return redirect(url_for('pos.pos'))

# ==========================================
# 4. ACTUALIZACIÓN DEL TICKET (Vinculado a la caja)
# ==========================================
@pos_bp.route('/ticket_pos', methods=['POST', 'GET'])
@roles_accepted('admin','ventas')
def ticket_pos():
    if request.method == 'POST':
        # Validar si la caja sigue abierta por seguridad
        sesion_activa = POSSesion.query.filter_by(usuario_id=current_user.id, estado='abierta').first()
        if not sesion_activa:
            flash('La caja está cerrada. Abre la caja para poder cobrar.', 'error')
            return redirect(url_for('pos.pos'))

        datos_carrito_str = request.form.get('datos_carrito')
        metodo_pago = request.form.get('metodo_pago')

        if not datos_carrito_str or datos_carrito_str == '[]':
            flash('El carrito está vacío. Agrega productos antes de cobrar.', 'error')
            return redirect(url_for('pos.pos'))

        try:
            carrito = json.loads(datos_carrito_str)
            total_venta = sum(item['subtotal'] for item in carrito)

            # ¡AQUÍ ESTÁ LA MAGIA! Le agregamos el sesion_id
            nueva_venta = Venta(
                usuario_id=current_user.id, 
                canal_venta='Mostrador',
                estado_pedido='Entregado', 
                total_venta=total_venta,
                metodo_pago_fisico=metodo_pago,
                sesion_id=sesion_activa.id # <---- VINCULAMOS LA VENTA AL TURNO
            )
            db.session.add(nueva_venta)
            db.session.flush() 

            resumen_venta = []
            # (El resto del código del carrito (for item in carrito...) se queda exactamente IGUAL que como lo tenías)
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

                    nombre_perfume = producto.receta.nombre_perfume if producto.receta else item['nombre']
                    presentacion = f"{producto.presentacion.nombre} {producto.presentacion.mililitros}ml" if producto.presentacion else ""
                    resumen_venta.append(f"{cantidad_vendida}x {nombre_perfume} {presentacion}")
                else:
                    db.session.rollback()
                    flash(f'Error: Stock insuficiente para {item["nombre"]}.', 'error')
                    return redirect(url_for('pos.pos'))

            texto_resumen = ", ".join(resumen_venta)
            registrar_log(
                accion="SALIDA",
                tabla="productos_terminados",
                registro_id=nueva_venta.id,
                detalle=f"Venta mostrador #{nueva_venta.id}: [ {texto_resumen} ]"
            )

            db.session.commit()
            
            return render_template('modulos_front/pos/ticket_pos.html', venta=nueva_venta)
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la venta: {str(e)}', 'error')
            return redirect(url_for('pos.pos'))
            
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
            db.session.flush() # Flush para obtener el ID de nueva_merma
            
            # 3. REGISTRO DE BITÁCORA: MERMA
            nombre_perfume = producto.receta.nombre_perfume if producto.receta else "Producto Desconocido"
            presentacion = f"{producto.presentacion.nombre} {producto.presentacion.mililitros}ml" if producto.presentacion else ""
            
            registrar_log(
                accion="MERMA",
                tabla="merma_inventario",
                registro_id=nueva_merma.id,
                detalle=f"Merma en Mostrador: -{cantidad} {nombre_perfume} {presentacion}. Razón: {motivo}"
            )
            
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
