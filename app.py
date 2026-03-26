from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from modulos_routes.inv_materias import invMP_bp

from models import db
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(invMP_bp)

csrf=CSRFProtect()
db.init_app(app)

# Prueba usuario
class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

@app.route('/')
def index():
    #Usuario de prueba aqui debe ir la consulta mysql
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    
    return render_template('index.html', current_user=usuario_logueado)

@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404

@app.context_processor
def inject_user():
    usuario_logueado = Usuario(nombre="Usuario", rol="Administrador")
    return dict(current_user=usuario_logueado)

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
