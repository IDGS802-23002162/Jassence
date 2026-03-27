
from flask import Blueprint, render_template, request
from sqlalchemy import extract, func
from models import db

ecommerce_bp=Blueprint('ecommerce',__name__)


@ecommerce_bp.route("/ecommerce", methods=["GET", "POST"])
def ecommerce():

    return render_template("modulos_front/ecommerce/ecommerce.html")
