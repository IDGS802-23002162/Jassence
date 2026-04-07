from . import compras_bp
import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from models import db, Proveedor, Compra, DetalleCompra, MateriaPrima
from datetime import datetime, timedelta
from flask_security import current_user, roles_accepted

@compras_bp.route('/proveedores')
@roles_accepted('admin','inventario') 
def proveedores():
    lista_proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('modulos_front/compras/proveedores.html', proveedores=lista_proveedores)

@compras_bp.route('/registrar_P', methods=['GET', 'POST'])
@roles_accepted('admin','inventario') 
def registrar_P():
    if request.method == 'POST':
        nombre_empresa = request.form.get('nombre_empresa')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        tipo_insumos = request.form.get('tipo_insumos')

        nuevo_proveedor = Proveedor(
            nombre_empresa=nombre_empresa,
            telefono=telefono,
            direccion=direccion,
            tipo_insumos=tipo_insumos,
            activo=True  
        )

        try:
            db.session.add(nuevo_proveedor)
            db.session.commit()
            flash('¡Proveedor registrado exitosamente!', 'success')
            return redirect(url_for('compras.proveedores')) 
        except Exception as e:
            db.session.rollback() 
            flash(f'Ocurrió un error: {str(e)}', 'error')
            
    return render_template('modulos_front/compras/registrar_P.html')


@compras_bp.route('/detalle_proveedor/<int:id>') 
@roles_accepted('admin','inventario') 
def detalle_P(id):
    proveedor = Proveedor.query.get_or_404(id)
    return render_template('modulos_front/compras/detalle_P.html', proveedor=proveedor)


@compras_bp.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin','inventario') 
def editar_P(id):
    proveedor = Proveedor.query.get_or_404(id)
    
    if request.method == 'POST':
        proveedor.nombre_empresa = request.form.get('nombre_empresa')
        proveedor.telefono = request.form.get('telefono')
        proveedor.direccion = request.form.get('direccion')
        proveedor.tipo_insumos = request.form.get('tipo_insumos')
        
        try:
            db.session.commit()
            flash('¡Proveedor actualizado con éxito!', 'success')
            return redirect(url_for('compras.proveedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
            
    return render_template('modulos_front/compras/editar_P.html', proveedor=proveedor)


@compras_bp.route('/eliminar_proveedor/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario') 
def baja_P(id):
    proveedor = Proveedor.query.get_or_404(id)
    try:
        proveedor.activo = False  
        db.session.commit()
        flash('Proveedor dado de baja exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al intentar dar de baja.', 'error')
        
    return redirect(url_for('compras.proveedores'))

# //////////////////////////////////////////////////////////////

@compras_bp.route('/compras')
@roles_accepted('admin','inventario') 
def compras():
    compras_pendientes = Compra.query.filter_by(estado='Pendiente').all()
    ahora = datetime.utcnow()
    tiempo_espera = timedelta(hours=1) 
    hubo_cambios = False

    for compra in compras_pendientes:
        if compra.fecha and ahora >= (compra.fecha + tiempo_espera):
            compra.estado = 'Recibido'
            
            for detalle in compra.detalles:
                mp = MateriaPrima.query.get(detalle.materia_prima_id)
                if mp:
                    # --- ACTUALIZADO CON GALONES ---
                    if detalle.unidad_compra == 'Litros':
                        cantidad_real = detalle.cantidad_comprada * 1000
                    elif detalle.unidad_compra == 'Galon Americano':
                        cantidad_real = detalle.cantidad_comprada * 3785.41
                    elif detalle.unidad_compra == 'Galon Imperial':
                        cantidad_real = detalle.cantidad_comprada * 4546.09
                    elif detalle.unidad_compra in ['Cajas', 'Caja', 'Lotes', 'Lote']:
                        cantidad_real = detalle.cantidad_comprada * detalle.multiplicador
                    else:
                        cantidad_real = detalle.cantidad_comprada
                        
                    mp.cantidad_disponible += cantidad_real
                    
            hubo_cambios = True

    if hubo_cambios:
        db.session.commit()

    lista_compras = Compra.query.order_by(Compra.fecha.desc()).all()
    return render_template('modulos_front/compras/compras.html', compras=lista_compras)


@compras_bp.route('/detalle_C/<int:id>')
@roles_accepted('admin','inventario') 
def detalle_C(id):
    compra = Compra.query.get_or_404(id)
    return render_template('modulos_front/compras/detalle_C.html', compra=compra) 


@compras_bp.route('/marcar_recibido/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario') 
def marcar_recibido(id):
    compra = Compra.query.get_or_404(id)
    
    if compra.estado == 'Pendiente':
        try:
            compra.estado = 'Recibido'
            
            for detalle in compra.detalles:
                mp = MateriaPrima.query.get(detalle.materia_prima_id)
                if mp:
                    # --- ACTUALIZADO CON GALONES ---
                    if detalle.unidad_compra == 'Litros':
                        cantidad_real = detalle.cantidad_comprada * 1000
                    elif detalle.unidad_compra == 'Galon Americano':
                        cantidad_real = detalle.cantidad_comprada * 3785.41
                    elif detalle.unidad_compra == 'Galon Imperial':
                        cantidad_real = detalle.cantidad_comprada * 4546.09
                    elif detalle.unidad_compra in ['Cajas', 'Caja', 'Lotes', 'Lote']:
                        cantidad_real = detalle.cantidad_comprada * detalle.multiplicador
                    else:
                        cantidad_real = detalle.cantidad_comprada
                        
                    mp.cantidad_disponible += cantidad_real
                    
            db.session.commit()
            flash('¡Mercancía recibida físicamente! El stock ha sido sumado al inventario en sus unidades correctas.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al procesar la entrada: {str(e)}', 'error')
    else:
        flash('Esta compra ya fue procesada anteriormente o está cancelada.', 'warning')
        
    return redirect(url_for('compras.compras'))


@compras_bp.route('/registrar_C', methods=['GET', 'POST'])
@roles_accepted('admin','inventario') 
def registrar_C():
    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        notas = request.form.get('notas', '')
        archivo = request.files.get('archivo_factura')
        
        materias_ids = request.form.getlist('materia_prima_id[]')
        cantidades = request.form.getlist('cantidad_comprada[]')
        unidades = request.form.getlist('unidad_compra[]')
        precios = request.form.getlist('precio_unitario[]')
        multiplicadores = request.form.getlist('multiplicador[]')

        nombre_archivo = None
        if archivo and archivo.filename != '':
            nombre_archivo = secure_filename(archivo.filename)
            ruta_carpeta = os.path.join('static', 'uploads', 'facturas')
            os.makedirs(ruta_carpeta, exist_ok=True)
            archivo.save(os.path.join(ruta_carpeta, nombre_archivo))

        nueva_compra = Compra(
            proveedor_id=proveedor_id,
            usuario_id=current_user.id, 
            archivo_factura=nombre_archivo,
            notas=notas,
            estado='Pendiente'
        )
        
        db.session.add(nueva_compra)
        db.session.flush() 

        total_compra = 0

        for i in range(len(materias_ids)):
            id_mp = materias_ids[i]
            cant_comprada = float(cantidades[i]) 
            prec = float(precios[i])
            
            mult = 1.0
            if multiplicadores and i < len(multiplicadores) and multiplicadores[i].strip():
                mult = float(multiplicadores[i])
            
            sub = cant_comprada * prec 
            total_compra += sub

            detalle = DetalleCompra(
                compra_id=nueva_compra.id,
                materia_prima_id=id_mp,
                cantidad_comprada=cant_comprada,
                unidad_compra=unidades[i],
                precio_unitario=prec,
                subtotal=sub,
                multiplicador=mult
            )
            db.session.add(detalle)

        nueva_compra.total = total_compra
        
        try:
            db.session.commit()
            flash('¡Compra registrada como PENDIENTE! El stock entrará cuando llegue el camión. UwU', 'success')
            return redirect(url_for('compras.compras'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la compra: {str(e)}', 'error')

    proveedores = Proveedor.query.filter_by(activo=True).all()
    materias = MateriaPrima.query.all()
    return render_template('modulos_front/compras/registrar_C.html', 
                           proveedores=proveedores, 
                           materias_primas=materias)


@compras_bp.route('/cancelar_compra/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario') 
def cancelar_C(id):
    compra = Compra.query.get_or_404(id)
    
    if compra.estado != 'cancelado':
        try:
            estado_anterior = compra.estado 
            compra.estado = 'cancelado'
            
            if estado_anterior == 'Recibido':
                for detalle in compra.detalles:
                    mp = MateriaPrima.query.get(detalle.materia_prima_id)
                    if mp:
                        # --- ACTUALIZADO CON GALONES ---
                        if detalle.unidad_compra == 'Litros':
                            cantidad_real = detalle.cantidad_comprada * 1000
                        elif detalle.unidad_compra == 'Galon Americano':
                            cantidad_real = detalle.cantidad_comprada * 3785.41
                        elif detalle.unidad_compra == 'Galon Imperial':
                            cantidad_real = detalle.cantidad_comprada * 4546.09
                        elif detalle.unidad_compra in ['Cajas', 'Caja', 'Lotes', 'Lote']:
                            cantidad_real = detalle.cantidad_comprada * detalle.multiplicador
                        else:
                            cantidad_real = detalle.cantidad_comprada
                            
                        mp.cantidad_disponible -= cantidad_real
                        
            db.session.commit()
            flash('Compra anulada correctamente. Inventario ajustado.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al anular.', 'error')
            
    return redirect(url_for('compras.compras'))


@compras_bp.route('/agregar_materia_rapida', methods=['POST'])
@roles_accepted('admin','inventario') 
def agregar_materia_rapida():
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    unidad_medida = request.form.get('unidad_medida')
    stock_minimo = float(request.form.get('stock_minimo', 0))
    
    nueva_materia = MateriaPrima(
        nombre=nombre,
        tipo=tipo,
        unidad_medida=unidad_medida,
        stock_minimo=stock_minimo,
        cantidad_disponible=0.0 
    )
    db.session.add(nueva_materia)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'id': nueva_materia.id,
        'nombre': nueva_materia.nombre,
        'unidad_medida': nueva_materia.unidad_medida
    })

@compras_bp.route('/actualizar_notas/<int:id>', methods=['POST'])
@roles_accepted('admin','inventario') 
def actualizar_notas(id):
    compra = Compra.query.get_or_404(id)
    
    if compra.estado == 'cancelado':
        flash('No se pueden modificar las notas de una compra anulada.', 'error')
        return redirect(url_for('compras.detalle_C', id=compra.id))

    nueva_nota = request.form.get('notas')
    
    try:
        compra.notas = nueva_nota
        db.session.commit()
        flash('¡Notas actualizadas y guardadas correctamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al guardar las notas.', 'error')
        
    return redirect(url_for('compras.detalle_C', id=compra.id))

# ///////////////////////////////////////////////////////////////////

@compras_bp.route('/historial_PC')
@roles_accepted('admin','inventario') 
def historial_PC():
    ahora = datetime.utcnow()
    tiempo_espera = timedelta(hours=1) 
    
    pendientes = Compra.query.filter_by(estado='Pendiente').all()
    hubo_cambios = False

    for compra in pendientes:
        if compra.fecha and ahora >= (compra.fecha + tiempo_espera):
            compra.estado = 'Recibido'
            for detalle in compra.detalles:
                mp = MateriaPrima.query.get(detalle.materia_prima_id)
                if mp:
                    # --- ACTUALIZADO CON GALONES ---
                    if detalle.unidad_compra == 'Litros':
                        cantidad_real = detalle.cantidad_comprada * 1000
                    elif detalle.unidad_compra == 'Galon Americano':
                        cantidad_real = detalle.cantidad_comprada * 3785.41
                    elif detalle.unidad_compra == 'Galon Imperial':
                        cantidad_real = detalle.cantidad_comprada * 4546.09
                    elif detalle.unidad_compra in ['Cajas', 'Caja', 'Lotes', 'Lote']:
                        cantidad_real = detalle.cantidad_comprada * detalle.multiplicador
                    else:
                        cantidad_real = detalle.cantidad_comprada
                        
                    mp.cantidad_disponible += cantidad_real
            hubo_cambios = True

    if hubo_cambios:
        db.session.commit()

    logs = Compra.query.order_by(Compra.fecha.desc()).all()
    proveedores = Proveedor.query.filter_by(activo=True).all()
    
    return render_template('modulos_front/compras/historial_PC.html', 
                           logs=logs, 
                           proveedores=proveedores)


@compras_bp.route('/detalle_H/<int:id>')
@roles_accepted('admin','inventario') 
def detalle_H(id):
    log = Compra.query.get_or_404(id)
    return render_template('modulos_front/compras/detalle_H.html', log=log)