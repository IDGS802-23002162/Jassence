from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g


from models import db
#Importe de rutas 
from modulos_routes.pos.routes import pos_bp
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf=CSRFProtect()
db.init_app(app)

app.register_blueprint(pos_bp)

#Registro de rutas 


class UsuarioFalso:
    nombre = "Erick"
    rol = "Admin"

@app.context_processor
def inyectar_usuario():
    # Esto envía el 'current_user' falso a TODOS los archivos HTML automáticamente
    return dict(current_user=UsuarioFalso())

@app.route('/')
def index():
    
    return render_template('index.html')

@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
