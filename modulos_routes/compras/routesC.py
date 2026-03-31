from . import compras_bp
from flask import render_template, request, redirect, url_for, flash
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
    return render_template('modulos_front/compras/compras.html')

@compras_bp.route('/detalle_C')
def detalle_C():
    return render_template('modulos_front/compras/detalle_C.html') 

@compras_bp.route('/editar_C')
def editar_C():
    return render_template('modulos_front/compras/editar_C.html')

@compras_bp.route('/registrar_C')
def registrar_C():
    return render_template('modulos_front/compras/registrar_C.html')




@compras_bp.route('/cancelar_compra/<int:id>', methods=['POST'])
def cancelar_C(id):
    compra = Compra.query.get_or_404(id)
    try:
        compra.estado = 'cancelado' # Usamos el campo estado de tu modelo
        db.session.commit()
        flash('Compra anulada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar la compra: {str(e)}', 'error')
        
    return redirect(url_for('compras.compras'))

# ///////////////////////////////////////////////////////////////////

@compras_bp.route('/historial_PC')
def historial_PC():
    return render_template('modulos_front/compras/historial_PC.html')

@compras_bp.route('/detalle_H')
def detalle_H():
    return render_template('modulos_front/compras/detalle_H.html')