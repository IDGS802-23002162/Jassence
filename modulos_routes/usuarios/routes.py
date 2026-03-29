from flask import Blueprint, render_template, request

usuarios_bp = Blueprint('usuarios', __name__)


# ==========================================
# SECCIÓN: USUARIOS
# ==========================================

@usuarios_bp.route("/usuarios", methods=["GET"])
def usuarios():
    return render_template("modulos_front/usuarios/usuarios.html")

@usuarios_bp.route("/insertarUsuario", methods=["GET", "POST"])
def insertarUsuario():
    # Mandamos 'accion' para que cambie el título, y 'datos=None' para que los campos salgan vacíos.
    return render_template("modulos_front/usuarios/insertar.html",  accion="Registrar", datos=None)

@usuarios_bp.route("/modificarUsuario", methods=["GET", "POST"])
def modificarUsuario():
    # Datos ficticios para probar el renderizado pre-llenado
    datos_usuario = {
        'nombre': 'Erick',
        'apellidos': 'Gómez',
        'email': 'erick@jassence.com',
        'telefono': '555-1234',
        'rol': 'Administrador'
    }
    return render_template("modulos_front/usuarios/modificar.html", accion="Modificar", datos=datos_usuario)

@usuarios_bp.route("/eliminarUsuario", methods=["GET", "POST"])
def eliminarUsuario():
    # Por ahora no hace nada xd, debe dar baja logica 
    return render_template()


# ==========================================
# SECCIÓN: ROLES
# ==========================================

@usuarios_bp.route("/roles", methods=["GET"])
def roles():
    return render_template("modulos_front/usuarios/roles/roles.html")

@usuarios_bp.route("/insertarRol", methods=["GET", "POST"])
def insertarRol():
    return render_template("modulos_front/usuarios/roles/insertar.html", accion="Crear", datos=None)

@usuarios_bp.route("/modificarRol", methods=["GET", "POST"])
def modificarRol():
    # Datos ficticios para el rol
    datos_rol = {
        'nombre_rol': 'Administrador',
        'permisos': 'Acceso Total'
    }
    return render_template("modulos_front/usuarios/roles/modificar.html", accion="Modificar", datos=datos_rol)

@usuarios_bp.route("/eliminarRol", methods=["GET", "POST"])
def eliminarRol():
    # Por ahora no hace nada xd, debe dar baja logica 
    return render_template()
