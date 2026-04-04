from models import db, CorteCaja, Venta
from . import finanzas_bp
from flask import render_template, request, redirect, url_for, flash
from datetime import date
from sqlalchemy import text

@finanzas_bp.route('/corte_caja', methods=['GET', 'POST'])
def corte_caja():
    usuario_id = 1  # Reemplaza por el ID del usuario logueado

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

    # Egresos: como no hay tabla 'egresos', tomamos corte previo del mismo usuario o cero
    ultimo_corte = db.session.query(CorteCaja)\
                    .filter_by(usuario_id=usuario_id)\
                    .order_by(CorteCaja.fecha.desc())\
                    .first()
    
    # Usamos egresos del último corte o 0
    total_egresos = ultimo_corte.egresos_gastos if ultimo_corte else 0
    egresos = [{"categoria": "Gastos previos", "cantidad": 1, "total": total_egresos}] if total_egresos else []

    # Calcular utilidad neta y efectivo esperado
    apertura_valor = ultimo_corte.efectivo_real if ultimo_corte else 0
    utilidad_neta = total_ventas - total_egresos
    efectivo_esperado = apertura_valor + total_ventas - total_egresos

    if request.method == 'POST':
        efectivo_real = float(request.form['efectivo_real'])
        diferencia = efectivo_real - efectivo_esperado

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