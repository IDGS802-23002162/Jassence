from . import inventarioP_bp
from flask import render_template, request, redirect, url_for

class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

@inventarioP_bp.route('/inventario_P')
def inventario_P():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/inv_P.html',
        current_user=usuario_logueado
    )

@inventarioP_bp.route('/detalle_P')
def detalle_P():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/detalle_P.html',
        current_user=usuario_logueado
    )

@inventarioP_bp.route('/eliminar_P')
def eliminar_P():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/eliminar_P.html',
        current_user=usuario_logueado
    )

# /////////////////////////////////////////////////////////////////////////////

@inventarioP_bp.route('/merma_Pmodel')
def merma_Pmodel():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/merma_Pmodel.html',
        current_user=usuario_logueado
    )

# /////////////////////////////////////////////////////////////////////////////

@inventarioP_bp.route('/inventario_PM')
def inventario_PM():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/inventario_PM.html',
        current_user=usuario_logueado
    )

@inventarioP_bp.route('/registrar_PM')
def registrar_PM():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/registrar_PM.html',
        current_user=usuario_logueado
    )

@inventarioP_bp.route('/detalle_Pmerma')
def detalle_Pmerma():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/detalle_Pmerma.html',
        current_user=usuario_logueado
    )

# /////////////////////////////////////////////////////////////////////////////

@inventarioP_bp.route('/historial_P')
def historial_P():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/historial_P.html',
        current_user=usuario_logueado
    )

@inventarioP_bp.route('/detalle_PH')
def detalle_PH():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return render_template(
        'modulos_front/inv_productos/detalle_PH.html',
        current_user=usuario_logueado
    )