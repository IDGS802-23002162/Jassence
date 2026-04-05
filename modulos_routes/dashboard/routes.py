from flask import Blueprint, render_template, request
from models import db, Venta, Cliente, DetalleVenta, Compra, ProductoTerminado, Receta, Presentacion
from sqlalchemy import func
from datetime import datetime
import math
from flask_security import roles_accepted

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@roles_accepted('admin')
def index_dashboard():
    # Capturamos lo que el usuario mande por la URL
    filtro = request.args.get('filtro')
    valor = request.args.get('valor')

    # ========================================================
    # A. PREPARAMOS LAS CONSULTAS BASE
    # ========================================================
    q_ventas = db.session.query(Venta)
    q_compras = db.session.query(Compra)
    q_clientes = db.session.query(Cliente)
    
    # Para filtrar detalles y productos vendidos por fecha, necesitamos unir la tabla Venta
    q_detalles = db.session.query(
        Receta.nombre_perfume, Presentacion.mililitros,
        func.sum(DetalleVenta.cantidad).label('total_cantidad'),
        func.sum(DetalleVenta.cantidad * DetalleVenta.precio_unitario).label('total_bruto')
    ).select_from(DetalleVenta).join(
        ProductoTerminado, DetalleVenta.producto_terminado_id == ProductoTerminado.id
    ).join(Receta, ProductoTerminado.receta_id == Receta.id
    ).join(Presentacion, ProductoTerminado.presentacion_id == Presentacion.id
    ).join(Venta, DetalleVenta.venta_id == Venta.id) # Unimos venta para saber la fecha

    q_prod_vendidos = db.session.query(func.sum(DetalleVenta.cantidad)).select_from(DetalleVenta).join(Venta, DetalleVenta.venta_id == Venta.id)

    # ========================================================
    # B. APLICAMOS LA MAGIA DEL TIEMPO (FILTROS)
    # ========================================================
    if filtro == 'dia' and valor:
        fecha_dt = datetime.strptime(valor, '%Y-%m-%d').date()
        q_ventas = q_ventas.filter(func.date(Venta.fecha) == fecha_dt)
        q_compras = q_compras.filter(func.date(Compra.fecha) == fecha_dt)
        q_clientes = q_clientes.filter(func.date(Cliente.fecha_registro) == fecha_dt)
        q_detalles = q_detalles.filter(func.date(Venta.fecha) == fecha_dt)
        q_prod_vendidos = q_prod_vendidos.filter(func.date(Venta.fecha) == fecha_dt)
        
    elif filtro == 'mes' and valor:
        anio, mes = valor.split('-')
        q_ventas = q_ventas.filter(func.extract('year', Venta.fecha) == anio, func.extract('month', Venta.fecha) == mes)
        q_compras = q_compras.filter(func.extract('year', Compra.fecha) == anio, func.extract('month', Compra.fecha) == mes)
        q_clientes = q_clientes.filter(func.extract('year', Cliente.fecha_registro) == anio, func.extract('month', Cliente.fecha_registro) == mes)
        q_detalles = q_detalles.filter(func.extract('year', Venta.fecha) == anio, func.extract('month', Venta.fecha) == mes)
        q_prod_vendidos = q_prod_vendidos.filter(func.extract('year', Venta.fecha) == anio, func.extract('month', Venta.fecha) == mes)
        
    elif filtro == 'anio' and valor:
        q_ventas = q_ventas.filter(func.extract('year', Venta.fecha) == valor)
        q_compras = q_compras.filter(func.extract('year', Compra.fecha) == valor)
        q_clientes = q_clientes.filter(func.extract('year', Cliente.fecha_registro) == valor)
        q_detalles = q_detalles.filter(func.extract('year', Venta.fecha) == valor)
        q_prod_vendidos = q_prod_vendidos.filter(func.extract('year', Venta.fecha) == valor)
        
    elif filtro == 'semana' and valor:
        try:
            # Convierte "2026-W14" a fechas reales de Lunes a Domingo
            inicio_sem = datetime.strptime(valor + '-1', '%G-W%V-%u').date()
            fin_sem = datetime.strptime(valor + '-7', '%G-W%V-%u').date()
            q_ventas = q_ventas.filter(func.date(Venta.fecha) >= inicio_sem, func.date(Venta.fecha) <= fin_sem)
            q_compras = q_compras.filter(func.date(Compra.fecha) >= inicio_sem, func.date(Compra.fecha) <= fin_sem)
            q_clientes = q_clientes.filter(func.date(Cliente.fecha_registro) >= inicio_sem, func.date(Cliente.fecha_registro) <= fin_sem)
            q_detalles = q_detalles.filter(func.date(Venta.fecha) >= inicio_sem, func.date(Venta.fecha) <= fin_sem)
            q_prod_vendidos = q_prod_vendidos.filter(func.date(Venta.fecha) >= inicio_sem, func.date(Venta.fecha) <= fin_sem)
        except ValueError:
            pass

    # ========================================================
    # 1. INGRESOS Y EGRESOS
    # ========================================================
    total_bruto = q_ventas.with_entities(func.sum(Venta.total_venta)).scalar() or 0.0
    total_neto = total_bruto / 1.16
    gastos_insumos = q_compras.with_entities(func.sum(Compra.total)).scalar() or 0.0
    utilidad_neta = total_neto - gastos_insumos

    # ========================================================
    # 2. META MENSUAL (Basada en Ventas Totales)
    # ========================================================
    meta_ventas = 20000.00
    porcentaje_meta = (total_bruto / meta_ventas) * 100 if total_bruto > 0 else 0
    porcentaje_meta = min(porcentaje_meta, 100) 
    posicion_bolita = 100 - porcentaje_meta

    # ========================================================
    # 3. OTROS INDICADORES
    # ========================================================
    compra_promedio = q_ventas.with_entities(func.avg(Venta.total_venta)).scalar() or 0.0
    nuevos_clientes = q_clientes.count()
    productos_vendidos = q_prod_vendidos.scalar() or 0

    # ========================================================
    # 4. PRODUCTOS MÁS VENDIDOS
    # ========================================================
    q_detalles = q_detalles.group_by(ProductoTerminado.id, Receta.nombre_perfume, Presentacion.mililitros)
    top_cantidad = q_detalles.order_by(func.sum(DetalleVenta.cantidad).desc()).all()
    top_ganancia = q_detalles.order_by(func.sum(DetalleVenta.cantidad * DetalleVenta.precio_unitario).desc()).all()

    # ========================================================
    # 5. TENDENCIA SEMANAL DE VENTAS (Siempre Mes Actual)
    # ========================================================
    ahora = datetime.now()
    ventas_mes = db.session.query(Venta).filter(
        func.extract('year', Venta.fecha) == ahora.year,
        func.extract('month', Venta.fecha) == ahora.month
    ).all()

    ventas_semanas = [0, 0, 0, 0, 0] 
    for v in ventas_mes:
        if not v.fecha: continue
        dia = v.fecha.day
        if dia <= 7: ventas_semanas[0] += v.total_venta
        elif dia <= 14: ventas_semanas[1] += v.total_venta
        elif dia <= 21: ventas_semanas[2] += v.total_venta
        elif dia <= 28: ventas_semanas[3] += v.total_venta
        else: ventas_semanas[4] += v.total_venta

    max_venta = max(ventas_semanas)
    escala_maxima = math.ceil(max_venta / 100.0) * 100 if max_venta > 0 else 400
    etiquetas_x = [0, escala_maxima * 0.25, escala_maxima * 0.50, escala_maxima * 0.75, escala_maxima]

    return render_template('modulos_front/dashboard/dashboard.html',
                           total_bruto=total_bruto, 
                           total_neto=total_neto, 
                           utilidad_neta=utilidad_neta,
                           meta_ventas=meta_ventas, 
                           porcentaje_meta=porcentaje_meta, 
                           posicion_bolita=posicion_bolita,
                           compra_promedio=compra_promedio, 
                           nuevos_clientes=nuevos_clientes, 
                           productos_vendidos=productos_vendidos,
                           top_cantidad=top_cantidad, 
                           top_ganancia=top_ganancia,
                           ventas_semanas=ventas_semanas, 
                           etiquetas_x=etiquetas_x, 
                           escala_maxima=escala_maxima,
                           filtro_actual=filtro, 
                           valor_actual=valor) # Mandamos estos dos para que los inputs no se borren