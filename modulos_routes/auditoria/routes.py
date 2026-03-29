from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
from models import db

auditorias_bp=Blueprint('auditorias',__name__)


@auditorias_bp.route("/auditoria", methods=['GET','POST'])
def auditoria():

	return render_template("modulos_front/auditoria/movInventarios.html")

@auditorias_bp.route("/auditoria/accesos", methods=['GET','POST'])
def accesos():

	return render_template("modulos_front/auditoria/movAccessos.html")

@auditorias_bp.route("/auditoria/usuarios", methods=['GET','POST'])
def usuarios():

	return render_template("modulos_front/auditoria/movUsuarios.html")