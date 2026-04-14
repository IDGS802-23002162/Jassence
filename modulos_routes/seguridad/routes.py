
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import extract, func
from flask_security import current_user, login_required
from models import db, Rol, Usuario, Cliente
from flask_security.utils import verify_password
from flask_security.signals import user_registered
from flask_login.signals import user_logged_out, user_logged_in
from modulos_routes.auditoria.utils import registrar_log


seguridad_bp=Blueprint('seguridad',__name__)


@user_registered.connect
def configurar_2fa_automatico(sender, user, **kwargs):
    user.tf_primary_method = 'email'

    rol_cliente = Rol.query.filter_by(name='cliente').first()
    if rol_cliente:
        user.roles.append(rol_cliente) 
    else:
        print("ADVERTENCIA: El rol 'cliente' no existe. Ejecuta inicializar_roles().")

    cliente_existente = Cliente.query.get(user.id)

    if not cliente_existente:
        nuevo_cliente = Cliente(
            id=user.id, 
        )
        db.session.add(nuevo_cliente)

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

# ==========================================
# SEÑALES DE AUDITORÍA (LOGINS / LOGOUTS)
# ==========================================

def log_acceso_exitoso(sender, user, **extra):
    es_cliente = any(rol.name == 'cliente' for rol in user.roles)
    if not es_cliente:
        registrar_log(
            accion='LOGIN',
            tabla='accesos',
            registro_id=user.id,
            detalle='Inicio de sesión exitoso'
        )

def log_cierre_sesion(sender, user, **extra):
    es_cliente = any(rol.name == 'cliente' for rol in user.roles)
    if not es_cliente:
        registrar_log(
            accion='LOGOUT',
            tabla='accesos',
            registro_id=user.id,
            detalle='Cierre de sesión manual'
        )

@seguridad_bp.before_app_request
def log_acceso_fallido():
    if request.endpoint == 'security.login' and request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = Usuario.query.filter_by(email=email).first()

            if user and not verify_password(password, user.password):
                es_cliente = any(rol.name == 'cliente' for rol in user.roles)
                
                if not es_cliente:
                    registrar_log(
                        accion='LOGIN_FALLIDO',
                        tabla='accesos',
                        registro_id=user.id,
                        detalle=f'Intento Fallido: Contraseña incorrecta para {user.email}'
                    )

user_logged_in.connect(log_acceso_exitoso)
user_logged_out.connect(log_cierre_sesion)