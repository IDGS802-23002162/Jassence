from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g


from models import db

from modulos_routes.formulas import formulas_bp
from modulos_routes.produccion import produccion_bp
from modulos_routes.dashboard import dashboard_bp
from modulos_routes.finanzas import finanzas_bp
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf=CSRFProtect()
db.init_app(app)


app.register_blueprint(formulas_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(finanzas_bp)



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
