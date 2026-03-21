from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g


from models import db
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf=CSRFProtect()
db.init_app(app)

@app.route('/')
def index():
    # ELIMINAR INDEX DE AQUI
    return render_template("index.html", titulo="Panel Principal")

@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
