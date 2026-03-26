from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from models import db
#Importe de rutas 
from modulos_routes.seguridad.routes import seguridad_bp
from modulos_routes.usuarios.routes import usuarios_bp
from modulos_routes.formulas import formulas_bp
 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

class UsuarioFalso:
    nombre = "Erick"
    rol = "Admin"

@app.context_processor
def inyectar_usuario():
    # Esto envía el 'current_user' falso a TODOS los archivos HTML automáticamente
    return dict(current_user=UsuarioFalso())

csrf=CSRFProtect()
db.init_app(app)


#Registro de rutas 

app.register_blueprint(seguridad_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(formulas_bp)
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

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()

