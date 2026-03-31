from . import compras_bp
from flask import render_template, request, redirect, url_for, flash


@compras_bp.route('/proveedores')
def proveedores():
    return render_template('modulos_front/compras/proveedores.html')

@compras_bp.route('/registrar_P')
def registrar_P():
    return render_template('modulos_front/compras/registrar_P.html')


@compras_bp.route('/detalle_proveedor') 
def detalle_P():
   
    proveedor_ficticio = {
        "id": 1,
        "nombre_empresa": "Envases de Vidrio S.A.",
        "telefono": "555-0123-456",
        "direccion": "Calle Falsa 123, Colonia Industrial, León, Gto.",
        "tipo_insumos": "Empaques"
    }
    
    return render_template('modulos_front/compras/detalle_P.html', proveedor=proveedor_ficticio)

@compras_bp.route('/editar_P')
def editar_P():

    proveedor_ficticio = {
        "id": 1,
        "nombre_empresa": "Envases de Vidrio S.A.",
        "telefono": "555-0123-456",
        "direccion": "Calle Falsa 123, Colonia Industrial, León, Gto.",
        "tipo_insumos": "Empaques"
    }
    
    return render_template('modulos_front/compras/editar_P.html',  proveedor=proveedor_ficticio)

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

@compras_bp.route('/modal_Celiminar')
def modal_Celiminar():
    return render_template('modulos_front/compras/modal_Celiminar.html')

# ///////////////////////////////////////////////////////////////////

@compras_bp.route('/historial_PC')
def historial_PC():
    return render_template('modulos_front/compras/historial_PC.html')

@compras_bp.route('/detalle_H')
def detalle_H():
    return render_template('modulos_front/compras/detalle_H.html')