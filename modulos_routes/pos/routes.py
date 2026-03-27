from flask import Blueprint, render_template, request, redirect, url_for

pos_bp = Blueprint('pos', __name__)

@pos_bp.route('/pos', methods=['GET'])
def index_formulas():
    return render_template('modulos_front/pos/pos.html', titulo="Venta Local")
