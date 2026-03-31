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
from modulos_routes.auditoria.routes import auditorias_bp
from modulos_routes.inv_productos import inventarioP_bp
from modulos_routes.produccion import produccion_bp
from modulos_routes.dashboard import dashboard_bp
from modulos_routes.pos.routes import pos_bp
from modulos_routes.compras import compras_bp
from modulos_routes.inv_materias import invMP_bp
from modulos_routes.ecommerce.routes import ecommerce_bp
from modulos_routes.finanzas import finanzas_bp 

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

app.register_blueprint(ecommerce_bp)
app.register_blueprint(invMP_bp)
app.register_blueprint(seguridad_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(formulas_bp)
app.register_blueprint(auditorias_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(inventarioP_bp) 
app.register_blueprint(compras_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(pos_bp)
app.register_blueprint(finanzas_bp)


# Ahora el index del sistema es /inicio
@app.route('/inicio')
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

