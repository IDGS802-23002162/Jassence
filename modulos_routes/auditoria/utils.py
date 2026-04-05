from models import db, LogAuditoria
from flask_security import current_user
from datetime import datetime

def registrar_log(accion, tabla, registro_id, detalle):
    # Verificamos si hay un usuario en sesión, de lo contrario registramos None (Ej. intentos fallidos)
    user_id = current_user.id
    
    nuevo_log = LogAuditoria(
        usuario_id=user_id,
        accion=accion,
        tabla_afectada=tabla,
        registro_id=registro_id,
        detalle=detalle,
        fecha=datetime.now()
    )
    db.session.add(nuevo_log)
    db.session.commit()