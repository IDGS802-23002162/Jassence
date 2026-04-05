from models import db, CorteCaja, Venta
from . import finanzas_bp
from flask import render_template, request, redirect, url_for, flash
from datetime import date
from flask_security import current_user, roles_accepted

@finanzas_bp.route('/corte_caja', methods=['GET', 'POST'])
@roles_accepted('admin','ventas')
def corte_caja():
    usuario_id = current_user.id # Reemplaza por el ID del usuario logueado

    # Obtener todas las ventas del día
    ventas_dia = db.session.query(Venta).filter(Venta.fecha >= date.today()).all()

    # Calcular totales por método de pago
    ingresos = {}
    total_ventas = 0
    for v in ventas_dia:
        metodo = v.metodo_pago_fisico or "Otro"
        if metodo not in ingresos:
            ingresos[metodo] = {"transacciones": 0, "total": 0}
        ingresos[metodo]["transacciones"] += 1
        ingresos[metodo]["total"] += v.total_venta
        total_ventas += v.total_venta

    # Obtener último corte del usuario
    ultimo_corte = db.session.query(CorteCaja)\
                    .filter_by(usuario_id=usuario_id)\
                    .order_by(CorteCaja.fecha.desc())\
                    .first()
    
    # Valor inicial de apertura (último efectivo_real o 0 si no hay corte)
    apertura_valor = ultimo_corte.efectivo_real if ultimo_corte else 0

    # Egresos del último corte o cero
    total_egresos = ultimo_corte.egresos_gastos if ultimo_corte else 0
    egresos = [{"categoria": "Gastos previos", "cantidad": 1, "total": total_egresos}] if total_egresos else []

    # Calcular utilidad neta y efectivo esperado
    utilidad_neta = total_ventas - total_egresos
    efectivo_esperado = apertura_valor + total_ventas - total_egresos

    if request.method == 'POST':
        apertura_valor = float(request.form['apertura'])
        efectivo_real = float(request.form['efectivo_real'])
        diferencia = efectivo_real - efectivo_esperado

        # Verificar si ya existe corte para hoy
        corte_existente = db.session.query(CorteCaja)\
                            .filter_by(usuario_id=usuario_id, fecha=date.today())\
                            .first()
        if corte_existente:
            # Actualizar corte existente
            corte_existente.apertura = apertura_valor
            corte_existente.ventas_totales = total_ventas
            corte_existente.egresos_gastos = total_egresos
            corte_existente.utilidad_neta = utilidad_neta
            corte_existente.efectivo_esperado = efectivo_esperado
            corte_existente.efectivo_real = efectivo_real
            corte_existente.diferencia = diferencia
            db.session.commit()
        else:
            # Crear nuevo corte
            corte = CorteCaja(
                usuario_id=usuario_id,
                fecha=date.today(),
                apertura=apertura_valor,
                ventas_totales=total_ventas,
                egresos_gastos=total_egresos,
                utilidad_neta=utilidad_neta,
                efectivo_esperado=efectivo_esperado,
                efectivo_real=efectivo_real,
                diferencia=diferencia
            )
            db.session.add(corte)
            db.session.commit()

        flash("Corte de caja cerrado con éxito!", "success")
        return redirect(url_for('finanzas.corte_caja'))

    return render_template(
        'modulos_front/finanzas/corte_caja.html',
        apertura=apertura_valor,
        ventas_totales=total_ventas,
        egresos_gastos=total_egresos,
        utilidad_neta=utilidad_neta,
        efectivo_esperado=efectivo_esperado,
        ingresos=ingresos,
        egresos=egresos
    )