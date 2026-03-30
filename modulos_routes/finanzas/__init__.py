from flask import Blueprint, render_template

finanzas_bp = Blueprint('finanzas', __name__)

@finanzas_bp.route('/corte_caja', methods=['GET'])
def index_corte():
    return render_template('modulos_front/finanzas/corte_caja.html')