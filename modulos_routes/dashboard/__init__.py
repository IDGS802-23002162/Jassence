from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

#  Ruta para el Dashboard
@dashboard_bp.route('/dashboard', methods=['GET'])
def index_dashboard():
    return render_template('modulos_front/dashboard/dashboard.html')