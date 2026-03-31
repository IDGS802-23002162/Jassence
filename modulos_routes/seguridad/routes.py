
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import extract, func
from flask_security import current_user, login_required
from models import db, Rol
from flask_security.signals import user_registered


seguridad_bp=Blueprint('seguridad',__name__)


@user_registered.connect
def configurar_2fa_automatico(sender, user, **kwargs):
    user.tf_primary_method = 'email'

    rol_cliente = Rol.query.filter_by(name='cliente').first()
    if rol_cliente:
        user.roles.append(rol_cliente) 
    else:
        print("ADVERTENCIA: El rol 'cliente' no existe. Ejecuta inicializar_roles().")

    db.session.commit()
    print(f"ÉXITO: 2FA por correo activado automáticamente para {user.email}")

@seguridad_bp.route('/check-role')
@login_required 
def check_role():
    roles_sistema = ['admin', 'ventas', 'produccion', 'inventario']
    if any(current_user.has_role(rol) for rol in roles_sistema):
        return redirect('/inicio')
    
    # Si no tiene roles de sistema, asumimos que es cliente y va a la tienda
    return redirect('/')