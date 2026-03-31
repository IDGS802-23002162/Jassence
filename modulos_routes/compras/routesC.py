from . import compras_bp
import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, current_app
from models import db, Proveedor, Compra, DetalleCompra, MateriaPrima

@compras_bp.route('/proveedores')
def proveedores():
    lista_proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('modulos_front/compras/proveedores.html', proveedores=lista_proveedores)

@compras_bp.route('/registrar_P', methods=['GET', 'POST'])
def registrar_P():
    if request.method == 'POST':
        # 1. Atrapamos los datos que vienen de los 'name' del HTML
        nombre_empresa = request.form.get('nombre_empresa')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        tipo_insumos = request.form.get('tipo_insumos')

        # 2. Construimos el nuevo objeto Proveedor
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
def detalle_P(id):

    proveedor = Proveedor.query.get_or_404(id)
    return render_template('modulos_front/compras/detalle_P.html', proveedor=proveedor)



@compras_bp.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
def editar_P(id):
    proveedor = Proveedor.query.get_or_404(id)
    
    if request.method == 'POST':
        # Sobreescribimos los datos actuales con los nuevos del formulario
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
def baja_P(id):
    proveedor = Proveedor.query.get_or_404(id)
    try:
        proveedor.activo = False  # Apagamos al proveedor sin borrar su historial
        db.session.commit()
        flash('Proveedor dado de baja exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al intentar dar de baja.', 'error')
        
    return redirect(url_for('compras.proveedores'))

# //////////////////////////////////////////////////////////////
@compras_bp.route('/compras')
def compras():
    lista_compras = Compra.query.order_by(Compra.fecha.desc()).all()
    return render_template('modulos_front/compras/compras.html', compras=lista_compras)

@compras_bp.route('/detalle_C/<int:id>')
def detalle_C(id):
    compra = Compra.query.get_or_404(id)
    return render_template('modulos_front/compras/detalle_C.html', compra=compra) 



@compras_bp.route('/editar_C/<int:id>', methods=['GET', 'POST'])
def editar_C(id):
    compra = Compra.query.get_or_404(id)
    
    if request.method == 'POST':
        compra.notas = request.form.get('notas')
        
        # Si sube un archivo nuevo, lo guardamos y actualizamos el nombre
        archivo = request.files.get('archivo_factura')
        if archivo and archivo.filename != '':
            nombre_archivo = secure_filename(archivo.filename)
            ruta_carpeta = os.path.join('static', 'uploads', 'facturas')
            os.makedirs(ruta_carpeta, exist_ok=True)
            archivo.save(os.path.join(ruta_carpeta, nombre_archivo))
            compra.archivo_factura = nombre_archivo
            
        try:
            db.session.commit()
            flash('¡Compra actualizada con éxito!', 'success')
            return redirect(url_for('compras.compras'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar.', 'error')
            
    return render_template('modulos_front/compras/editar_C.html', compra=compra)


@compras_bp.route('/registrar_C', methods=['GET', 'POST'])
def registrar_C():
    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        notas = request.form.get('notas', '')
        archivo = request.files.get('archivo_factura')
        
        materias_ids = request.form.getlist('materia_prima_id[]')
        cantidades = request.form.getlist('cantidad_comprada[]')
        unidades = request.form.getlist('unidad_compra[]')
        precios = request.form.getlist('precio_unitario[]')

        # 2. Manejo del Archivo PDF
        nombre_archivo = None
        if archivo and archivo.filename != '':
            nombre_archivo = secure_filename(archivo.filename)
            ruta_carpeta = os.path.join('static', 'uploads', 'facturas')
            # Creamos la carpeta si no existe
            os.makedirs(ruta_carpeta, exist_ok=True)
            archivo.save(os.path.join(ruta_carpeta, nombre_archivo))

        # 3. Creamos la cabecera de la Compra
        # Nota: Aquí usamos el ID 1 de usuario como prueba, luego usarás el de la sesión
        nueva_compra = Compra(
            proveedor_id=proveedor_id,
            usuario_id=1, 
            archivo_factura=nombre_archivo,
            notas=notas,
            estado='entregado'
        )
        
        db.session.add(nueva_compra)
        db.session.flush() # Esto nos da el ID de la compra antes del commit final

        total_compra = 0

        # Atrapamos la nueva lista del HTML
        cantidades_convertidas = request.form.getlist('cantidad_convertida[]')

        # 4. Procesamos cada insumo del detalle
        for i in range(len(materias_ids)):
            id_mp = materias_ids[i]
            cant_comprada = float(cantidades[i]) # Ej: 2 (Cajas)
            prec = float(precios[i])
            cant_real_inventario = float(cantidades_convertidas[i]) # Ej: 100 (Botellas totales)
            
            sub = cant_comprada * prec # El precio suele ser por la unidad de compra (ej. $300 por caja)
            total_compra += sub

            # Creamos el registro del detalle
            detalle = DetalleCompra(
                compra_id=nueva_compra.id,
                materia_prima_id=id_mp,
                cantidad_comprada=cant_comprada,
                unidad_compra=unidades[i],
                precio_unitario=prec,
                subtotal=sub,
                cantidad_convertida=cant_real_inventario # Guardamos la conversión para el historial
            )
            db.session.add(detalle)

            # 5. ACTUALIZACIÓN DE STOCK (¡Usamos la cantidad convertida!)
            mp = MateriaPrima.query.get(id_mp)
            if mp:
                mp.cantidad_disponible += cant_real_inventario # Sumamos 100 botellas, no 2 cajas

        nueva_compra.total = total_compra
        
        try:
            db.session.commit()
            flash('¡Compra y stock actualizados correctamente! UwU', 'success')
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
def cancelar_C(id):
    compra = Compra.query.get_or_404(id)
    
    if compra.estado != 'cancelado':
        try:
            compra.estado = 'cancelado'
            
            for detalle in compra.detalles:
                mp = MateriaPrima.query.get(detalle.materia_prima_id)
                if mp:
                    mp.cantidad_disponible -= detalle.cantidad_convertida
                    
            db.session.commit()
            flash('Compra anulada y stock revertido correctamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al anular.', 'error')
            
    return redirect(url_for('compras.compras'))

# ///////////////////////////////////////////////////////////////////

@compras_bp.route('/historial_PC')
def historial_PC():
    # Traemos todas las transacciones ordenadas por fecha
    logs = Compra.query.order_by(Compra.fecha.desc()).all()
    proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('modulos_front/compras/historial_PC.html', logs=logs, proveedores=proveedores)


@compras_bp.route('/detalle_H/<int:id>')
def detalle_H(id):
    # Buscamos el log específico
    log = Compra.query.get_or_404(id)
    return render_template('modulos_front/compras/detalle_H.html', log=log)