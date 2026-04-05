from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore
from forms import CustomRegisterForm, CustomLoginForm
from flask_mailman import Mail
from flask_security import auth_required, current_user, roles_required, roles_accepted
from initRoles import inicializar_roles
from flask import g

from models import db, Usuario, Rol

# Importe de rutas 
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

db.init_app(app)
csrf = CSRFProtect(app)
mail = Mail(app)

user_datastore = SQLAlchemyUserDatastore(db, Usuario, Rol)
security = Security(app, user_datastore, register_form=CustomRegisterForm, login_form=CustomLoginForm, mail_util=mail)


# Registro de rutas 
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

# Rutas principales
@app.route('/inicio')
@roles_accepted('admin', 'ventas', 'produccion', 'inventario')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e): 
    return render_template("404.html"), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        inicializar_roles()
    print("Tablas creadas con éxito.")
    app.run()
