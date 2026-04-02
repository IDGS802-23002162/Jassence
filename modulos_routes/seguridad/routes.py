
from flask import Blueprint, render_template, request
from sqlalchemy import extract, func
from models import db

seguridad_bp=Blueprint('seguridad',__name__)

# Prueba usuario
class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

@seguridad_bp.route("/login", methods=["GET", "POST"])
def login():

    #Usuario de prueba a eliminar porque no es el mismo layout
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")

    return render_template("modulos_front/seguridad/login.html", current_user=usuario_logueado)

@seguridad_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
     #Usuario de prueba a eliminar porque no es el mismo layout
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")

    return render_template("modulos_front/seguridad/registrar.html", current_user=usuario_logueado)
