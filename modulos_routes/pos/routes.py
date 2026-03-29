from flask import Blueprint, render_template, request, redirect, url_for

pos_bp = Blueprint('pos', __name__)

@pos_bp.route('/pos', methods=['GET'])
def index_formulas():
    return render_template('modulos_front/pos/pos.html', titulo="Venta Local")

@pos_bp.route('/ticket')
def ticket():
    return render_template('modulos_front/pos/ticket.html', titulo="Venta Local")

@pos_bp.route('/historial_V')
def historial_V():
    return render_template('modulos_front/pos/historial_V.html', titulo="Venta Local")

@pos_bp.route('/detalle_V')
def detalle_V():
    return render_template('modulos_front/pos/detalle_V.html', titulo="Venta Local")


