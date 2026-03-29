
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import extract, func
from models import db

ecommerce_bp=Blueprint('ecommerce',__name__)


@ecommerce_bp.route("/ecommerce", methods=["GET", "POST"])
def ecommerce():

    return render_template("modulos_front/ecommerce/ecommerce.html")

@ecommerce_bp.route("/pagar", methods=["GET", "POST"])
def pagar():

    if request.method == "POST": 
        return redirect(url_for('ecommerce.ticket'))

    return render_template("modulos_front/ecommerce/pago.html")


@ecommerce_bp.route("/ticket", methods=["GET", "POST"])
def ticket():

    return render_template("modulos_front/ecommerce/ticket.html")