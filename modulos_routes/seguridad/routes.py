
from flask import Blueprint, render_template, request
from sqlalchemy import extract, func
from models import db
from flask_security.signals import user_registered


seguridad_bp=Blueprint('seguridad',__name__)


@user_registered.connect
def configurar_2fa_automatico(sender, user, **kwargs):
    user.tf_primary_method = 'email'

    db.session.commit()
    print(f"ÉXITO: 2FA por correo activado automáticamente para {user.email}")