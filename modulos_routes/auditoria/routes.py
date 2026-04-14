from flask import Blueprint, render_template
from models import db, LogAuditoria, Usuario, Rol
from flask_security import roles_required, current_user
from datetime import date

auditorias_bp = Blueprint('auditorias', __name__)

# ==========================================
# RUTA 1: AUDITORÍA DE INVENTARIOS
# ==========================================
@auditorias_bp.route("/auditoria", methods=['GET'])
@roles_required('admin') 
def auditoria():
    tablas_inventario = ['materias_primas', 'productos_terminados', 'merma_inventario(PRODUCTO)', 'merma_inventario(MP)']
    logs = LogAuditoria.query.filter(LogAuditoria.tabla_afectada.in_(tablas_inventario))\
                             .order_by(LogAuditoria.fecha.desc()).all()

    stats = {
        'productos': LogAuditoria.query.filter_by(tabla_afectada='productos_terminados', accion='ENTRADA').count(),
        'materia_prima': LogAuditoria.query.filter_by(tabla_afectada='materias_primas', accion='ENTRADA').count(),
        'mermas': LogAuditoria.query.filter_by(tabla_afectada='merma_inventario(MP)').count() + LogAuditoria.query.filter_by(tabla_afectada='merma_inventario(Producto)').count()
    }
    
    return render_template("modulos_front/auditoria/movInventarios.html", logs=logs, stats=stats)


# ==========================================
# RUTA 2: AUDITORÍA DE ACCESOS
# ==========================================
@auditorias_bp.route("/auditoria/accesos", methods=['GET'])
@roles_required('admin')
def accesos():

    logs = LogAuditoria.query.filter(
    LogAuditoria.tabla_afectada == 'accesos'
    ).order_by(LogAuditoria.fecha.desc()).all()

    # Contadores para las cards
    hoy = date.today()
    stats = {
    'accesos_hoy': LogAuditoria.query.filter(
        LogAuditoria.tabla_afectada == 'accesos',
        LogAuditoria.accion == 'LOGIN',
        db.func.date(LogAuditoria.fecha) == hoy
    ).count(),

    'salidas_hoy': LogAuditoria.query.filter(
        LogAuditoria.tabla_afectada == 'accesos',
        LogAuditoria.accion == 'LOGOUT',
        db.func.date(LogAuditoria.fecha) == hoy
    ).count(),

    'fallidos': LogAuditoria.query.filter(
        LogAuditoria.tabla_afectada == 'accesos',
        LogAuditoria.accion == 'LOGIN_FALLIDO',
        db.func.date(LogAuditoria.fecha) == hoy
    ).count(),
    }

    return render_template("modulos_front/auditoria/movAccessos.html", logs=logs, stats=stats)


# ==========================================
# RUTA 3: AUDITORÍA DE USUARIOS
# ==========================================
@auditorias_bp.route("/auditoria/usuarios", methods=['GET'])
@roles_required('admin')
def usuarios():

    logs = LogAuditoria.query.filter_by(tabla_afectada='usuarios')\
                             .order_by(LogAuditoria.fecha.desc()).all()

    stats = {
        'altas': LogAuditoria.query.filter_by(tabla_afectada='usuarios', accion='CREATE').count(),
        'bajas': LogAuditoria.query.filter_by(tabla_afectada='usuarios', accion='DELETE').count(),
        'updates': LogAuditoria.query.filter_by(tabla_afectada='usuarios', accion='UPDATE').count(),
            
    }

    return render_template("modulos_front/auditoria/movUsuarios.html", logs=logs, stats=stats)

# ==========================================
# RUTA 1: AUDITORÍA DE INVENTARIOS
# ==========================================
@auditorias_bp.route("/auditoria/formulas", methods=['GET'])
@roles_required('admin') 
def formulas():
    tablas_formulas = ['recetas']
    logs = LogAuditoria.query.filter(LogAuditoria.tabla_afectada.in_(tablas_formulas))\
                             .order_by(LogAuditoria.fecha.desc()).all()

    stats = {
        'formulas_creadas': LogAuditoria.query.filter_by(tabla_afectada='recetas', accion='CREATE').count(),
        'formulas_eliminadas': LogAuditoria.query.filter_by(tabla_afectada='recetas', accion='DELETE').count(),
        'modificaciones': LogAuditoria.query.filter_by(tabla_afectada='recetas', accion='UPDATE').count(),
            
    }
    
    return render_template("modulos_front/auditoria/movFormulas.html", logs=logs, stats=stats)

