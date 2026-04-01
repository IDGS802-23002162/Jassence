import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security import roles_required, hash_password, current_user
from models import db, Usuario, Rol

usuarios_bp = Blueprint('usuarios', __name__)

# ==========================================
# SECCIÓN: USUARIOS
# ==========================================

@usuarios_bp.route("/usuarios", methods=["GET"])
@roles_required('admin')
def usuarios():
    # Traemos todos los usuarios reales
    lista_usuarios = Usuario.query.all()
    return render_template("modulos_front/usuarios/usuarios.html", usuarios=lista_usuarios)


@usuarios_bp.route("/usuarios/clientes", methods=["GET"])
@roles_required('admin')
def usuarios_clientes():
    # Traemos todos los usuarios reales
    lista_usuarios = Usuario.query.all()
    return render_template("modulos_front/usuarios/clientes.html", usuarios=lista_usuarios)

@usuarios_bp.route('/insertarUsuario', methods=['GET', 'POST'])
@roles_required('admin')
def insertar_usuario():
    from app import user_datastore # Importación local para evitar ciclos
    
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        telefono = request.form.get('telefono')
        nombre_rol = request.form.get('rol') 

        if user_datastore.find_user(email=email):
            flash('El correo ya está registrado en el sistema.', 'error')
            return redirect(url_for('usuarios.insertar_usuario'))

        # Crear el usuario con contraseña temporal
        password_temporal = "TEMP-" + os.urandom(4).hex()
        
        nuevo_usuario = user_datastore.create_user(
            email=email,
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            password=hash_password(password_temporal),
            active=True
        )

        # Asignar el rol seleccionado
        rol = user_datastore.find_role(nombre_rol)
        if rol:
            user_datastore.add_role_to_user(nuevo_usuario, rol)

        db.session.commit()

        # Enviar correo para que el usuario ponga su propia contraseña
        from flask_security.recoverable import send_reset_password_instructions
        send_reset_password_instructions(nuevo_usuario)
        
        flash(f'Usuario {email} creado exitosamente. Se envió correo de activación.', 'success')
        return redirect(url_for('usuarios.usuarios'))
        
    lista_roles = Rol.query.all()
    return render_template('modulos_front/usuarios/insertar.html', 
                           accion='Insertar', 
                           lista_roles=lista_roles)

@usuarios_bp.route("/modificarUsuario/<int:id>", methods=["GET", "POST"])
@roles_required('admin')
def modificar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    lista_roles = Rol.query.all()

    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        usuario.apellidos = request.form.get('apellidos')
        usuario.email = request.form.get('email')
        usuario.telefono = request.form.get('telefono')
        nuevo_rol_nombre = request.form.get('rol')
        
        # Actualizar Rol
        from app import user_datastore
        rol_nuevo = user_datastore.find_role(nuevo_rol_nombre)
        if rol_nuevo:
            usuario.roles = [rol_nuevo]
        
        db.session.commit()
        flash(f'Datos de {usuario.nombre} actualizados correctamente.', 'success')
        return redirect(url_for('usuarios.usuarios'))

    return render_template("modulos_front/usuarios/modificar.html", 
                           accion="Modificar", 
                           datos=usuario, 
                           lista_roles=lista_roles)

@usuarios_bp.route("/eliminarUsuario", methods=["POST"])
@roles_required('admin')
def eliminar_usuario():
    id_usuario = request.form.get('id')
    usuario = Usuario.query.get(id_usuario)
    
    if usuario:
        if usuario.id == current_user.id:
            flash('No puedes desactivar tu propia cuenta.', 'error')
        else:
            usuario.active = False  # Baja lógica
            db.session.commit()
            flash(f'Usuario {usuario.email} desactivado.', 'success')
            
    return redirect(url_for('usuarios.usuarios'))

@usuarios_bp.route("/reactivarUsuario", methods=["POST"])
@roles_required('admin')
def reactivar_usuario():
    id_usuario = request.form.get('id')
    usuario = Usuario.query.get(id_usuario)
    
    if usuario:
        usuario.active = True  # Reactivación lógica
        db.session.commit()
        flash(f'Usuario {usuario.email} ha sido reactivado.', 'success')
            
    return redirect(url_for('usuarios.usuarios'))


# ==========================================
# SECCIÓN: ROLES
# ==========================================

@usuarios_bp.route("/roles", methods=["GET"])
@roles_required('admin')
def gestion_roles():
    lista_roles = Rol.query.all()
    return render_template("modulos_front/usuarios/roles/roles.html", roles=lista_roles)

@usuarios_bp.route("/modificarRol/<int:id>", methods=["GET", "POST"])
@roles_required('admin')
def modificar_rol(id):
    rol = Rol.query.get_or_404(id)
    
    if request.method == 'POST':
        rol.description = request.form.get('descripcion')
        db.session.commit()
        flash(f'Descripción del rol {rol.name} actualizada.', 'success')
        return redirect(url_for('usuarios.gestion_roles'))

    return render_template("modulos_front/usuarios/roles/modificar.html", 
                           accion="Modificar", 
                           datos=rol)