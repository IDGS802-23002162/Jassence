from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, CorteCaja, Venta, POSSesion, EgresoCaja # <--- IMPORTA LOS NUEVOS MODELOS
from datetime import date, datetime
from flask_security import current_user, roles_accepted
from . import finanzas_bp

@finanzas_bp.route('/corte_caja', methods=['GET', 'POST'])
@roles_accepted('admin','ventas')
def corte_caja():
    usuario_id = current_user.id

    # 1. Buscamos el turno (sesión) que está actualmente abierto
    sesion_activa = POSSesion.query.filter_by(usuario_id=usuario_id, estado='abierta').first()
    
    # Si no hay caja abierta, mandamos todo en ceros
    if not sesion_activa:
        flash('No tienes ninguna caja abierta en este momento.', 'info')
        return render_template('modulos_front/finanzas/corte_caja.html', 
                               apertura=0, ventas_totales=0, egresos_gastos=0, 
                               utilidad_neta=0, efectivo_esperado=0, 
                               ingresos={}, egresos=[], sin_caja=True)

    # 2. Obtener SOLO las ventas vinculadas a ESTA sesión
    ventas_sesion = Venta.query.filter_by(sesion_id=sesion_activa.id).all()

    # Calcular totales por método de pago
    ingresos = {}
    total_ventas = 0
    for v in ventas_sesion:
        metodo = v.metodo_pago_fisico or "Otro"
        if metodo not in ingresos:
            ingresos[metodo] = {"transacciones": 0, "total": 0}
        ingresos[metodo]["transacciones"] += 1
        ingresos[metodo]["total"] += v.total_venta
        total_ventas += v.total_venta

    # 3. Obtener SOLO los egresos (retiros) vinculados a ESTA sesión
    egresos_sesion = EgresoCaja.query.filter_by(sesion_id=sesion_activa.id).all()
    total_egresos = sum(e.monto for e in egresos_sesion)
    
    # Formatear egresos para la tabla del HTML
    lista_egresos = [{"categoria": e.motivo, "cantidad": 1, "total": e.monto} for e in egresos_sesion]

    apertura_valor = sesion_activa.monto_apertura
    utilidad_neta = total_ventas - total_egresos
    efectivo_esperado = apertura_valor + total_ventas - total_egresos

    if request.method == 'POST':
        efectivo_real = float(request.form['efectivo_real'])
        diferencia = efectivo_real - efectivo_esperado

        # 4. Crear el registro del Corte
        corte = CorteCaja(
            usuario_id=usuario_id,
            sesion_id=sesion_activa.id, # Vinculamos el corte a la sesión
            fecha=datetime.utcnow().date(),
            apertura=apertura_valor,
            ventas_totales=total_ventas,
            egresos_gastos=total_egresos,
            utilidad_neta=utilidad_neta,
            efectivo_esperado=efectivo_esperado,
            efectivo_real=efectivo_real,
            diferencia=diferencia
        )
        db.session.add(corte)

        # ¡EL PASO MÁGICO! Cerramos la sesión
        sesion_activa.estado = 'cerrada'
        sesion_activa.cerrada_en = datetime.utcnow()

        db.session.commit()

        flash("¡Corte de caja realizado con éxito! El POS se ha bloqueado.", "success")
        return redirect(url_for('finanzas.corte_caja'))

    return render_template(
        'modulos_front/finanzas/corte_caja.html',
        apertura=apertura_valor,
        ventas_totales=total_ventas,
        egresos_gastos=total_egresos,
        utilidad_neta=utilidad_neta,
        efectivo_esperado=efectivo_esperado,
        ingresos=ingresos,
        egresos=lista_egresos,
        sin_caja=False
    )