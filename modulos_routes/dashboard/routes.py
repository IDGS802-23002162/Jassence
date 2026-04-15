from flask import Blueprint, render_template, request
from models import DetalleCompra, db, Venta, Cliente, DetalleVenta, Compra, ProductoTerminado, Receta, Presentacion
from sqlalchemy import func
from datetime import datetime, timedelta
import math
from flask_security import roles_accepted


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@roles_accepted('admin')
def index_dashboard():
    filtro = request.args.get('filtro')
    valor = request.args.get('valor')

    # ========================================================
    # A. PREPARAMOS LAS CONSULTAS BASE (FILTRO CANCELADO)
    # ========================================================
    q_ventas = db.session.query(Venta).filter(Venta.estado_pedido != 'Cancelado')
    q_compras = db.session.query(Compra)
    q_clientes = db.session.query(Cliente)
    
    q_detalles = db.session.query(
        Receta.id.label('receta_id'),
        Presentacion.id.label('presentacion_id'),
        Receta.nombre_perfume, 
        Presentacion.mililitros,
        func.sum(DetalleVenta.cantidad).label('total_cantidad'),
        func.sum(DetalleVenta.cantidad * DetalleVenta.precio_unitario).label('total_bruto')
    ).select_from(DetalleVenta).join(
        ProductoTerminado, DetalleVenta.producto_terminado_id == ProductoTerminado.id
    ).join(Receta, ProductoTerminado.receta_id == Receta.id
    ).join(Presentacion, ProductoTerminado.presentacion_id == Presentacion.id
    ).join(Venta, DetalleVenta.venta_id == Venta.id).filter(Venta.estado_pedido != 'Cancelado')

    q_prod_vendidos = db.session.query(func.sum(DetalleVenta.cantidad)).select_from(DetalleVenta).join(Venta, DetalleVenta.venta_id == Venta.id).filter(Venta.estado_pedido != 'Cancelado')

    
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
    utilidad_neta =  max(0.0, total_neto - gastos_insumos)

    # ========================================================
    # 2. META MENSUAL
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
    # 4. PRODUCTOS MÁS VENDIDOS (🔥 CON COSTOS REALES 🔥)
    # ========================================================
    q_detalles = q_detalles.group_by(Receta.id, Presentacion.id, Receta.nombre_perfume, Presentacion.mililitros)
    datos_agrupados = q_detalles.all()

    lista_productos = []
    for prod in datos_agrupados:
        cantidad_vendida = float(prod.total_cantidad)
        bruto_vendido = float(prod.total_bruto)
        costo_unitario = float(calcular_costo_produccion(prod.receta_id, prod.presentacion_id))

        # 🔥 NUEVO: Utilidad Unitaria (Lo que le ganas a 1 frasco) 🔥
        # Calculamos el ingreso de un solo frasco sin IVA
        ingreso_neto_unitario = (bruto_vendido / cantidad_vendida) / 1.16 if cantidad_vendida > 0 else 0
        utilidad_unitaria = ingreso_neto_unitario - costo_unitario
        
        costo_total_prod = costo_unitario * cantidad_vendida
        #Ingreso Neto (sin IVA)
        ingreso_neto_prod = bruto_vendido / 1.16
        
        utilidad_real = ingreso_neto_prod - costo_total_prod

        lista_productos.append({
            'nombre_perfume': prod.nombre_perfume,
            'mililitros': prod.mililitros,
            'total_cantidad': prod.total_cantidad,
            'total_bruto': prod.total_bruto,
            'costo_unitario': costo_unitario,
            'utilidad_unitaria': utilidad_unitaria, # Mandamos la ganancia de 1 producto al HTML
            'utilidad_real': utilidad_real
        })

    top_cantidad = sorted(lista_productos, key=lambda x: x['total_cantidad'], reverse=True)
    top_ganancia = sorted(lista_productos, key=lambda x: x['utilidad_real'], reverse=True)
    top_bruto = sorted(lista_productos, key=lambda x: x['total_bruto'], reverse=True)

    # ========================================================
    # 5. TENDENCIA SEMANAL DE VENTAS
    # ========================================================
    ahora = datetime.now()
    ventas_mes = db.session.query(Venta).filter(
        func.extract('year', Venta.fecha) == ahora.year,
        func.extract('month', Venta.fecha) == ahora.month,
        Venta.estado_pedido != 'Cancelado' # ¡No olvidamos el filtro aquí tampoco!
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
                           gastos_insumos=gastos_insumos,
                           meta_ventas=meta_ventas, 
                           porcentaje_meta=porcentaje_meta, 
                           posicion_bolita=posicion_bolita,
                           compra_promedio=compra_promedio, 
                           nuevos_clientes=nuevos_clientes, 
                           productos_vendidos=productos_vendidos,
                           top_cantidad=top_cantidad, 
                           top_ganancia=top_ganancia,
                           top_bruto=top_bruto,
                           ventas_semanas=ventas_semanas, 
                           etiquetas_x=etiquetas_x, 
                           escala_maxima=escala_maxima,
                           filtro_actual=filtro, 
                           valor_actual=valor)



def obtener_costo_promedio_insumo(item_id, tipo_item='materia', dias_margen=60):
    """
    Calcula el costo promedio por ML o por Unidad de un insumo.
    Convierte automáticamente los Litros a Mililitros para evitar sobrecostos.
    """
    fecha_limite = datetime.utcnow() - timedelta(days=dias_margen)

    # Obtenemos las compras recientes del insumo
    query = DetalleCompra.query.join(Compra).filter(
        Compra.fecha >= fecha_limite,
        Compra.estado != 'cancelado',
        DetalleCompra.tipo_item == tipo_item
    )

    if tipo_item == 'materia':
        query = query.filter(DetalleCompra.materia_prima_id == item_id)
    else:
        query = query.filter(DetalleCompra.presentacion_id == item_id)

    compras_recientes = query.all()

    # Variables para sacar el promedio
    costo_total = 0.0
    cantidad_total_estandarizada = 0.0

    if compras_recientes:
        for detalle in compras_recientes:
            costo_total += detalle.subtotal
            cantidad_real = detalle.cantidad_comprada

            # 🔥 EL FIX PRINCIPAL: Estandarizar a Mililitros
            if tipo_item == 'materia':
                unidad = (detalle.unidad_compra or '').lower().strip()
                # Si compró en Litros, lo pasamos a ML
                if unidad in ['litro', 'litros', 'l', 'lt']:
                    cantidad_real = cantidad_real * 1000
                # Si el multiplicador está configurado y es mayor a 1, lo usamos
                elif detalle.multiplicador and detalle.multiplicador > 1.0:
                    cantidad_real = cantidad_real * detalle.multiplicador

            cantidad_total_estandarizada += cantidad_real

        # Retornamos el costo promedio (Ej: $125 / 1000ml = $0.125 por ml)
        if cantidad_total_estandarizada > 0:
            return costo_total / cantidad_total_estandarizada

    # ==========================================
    # FALLBACK: Si no hay compras recientes, buscar la más vieja
    # ==========================================
    ultima_compra_query = DetalleCompra.query.join(Compra).filter(
        Compra.estado != 'cancelado',
        DetalleCompra.tipo_item == tipo_item
    )

    if tipo_item == 'materia':
        ultima_compra_query = ultima_compra_query.filter(DetalleCompra.materia_prima_id == item_id)
    else:
        ultima_compra_query = ultima_compra_query.filter(DetalleCompra.presentacion_id == item_id)

    ultima_compra = ultima_compra_query.order_by(Compra.fecha.desc()).first()

    if ultima_compra and ultima_compra.cantidad_comprada > 0:
        cantidad_real = ultima_compra.cantidad_comprada
        
        if tipo_item == 'materia':
            unidad = (ultima_compra.unidad_compra or '').lower().strip()
            if unidad in ['litro', 'litros', 'l', 'lt']:
                cantidad_real = cantidad_real * 1000
            elif ultima_compra.multiplicador and ultima_compra.multiplicador > 1.0:
                cantidad_real = cantidad_real * ultima_compra.multiplicador
                
        return ultima_compra.subtotal / cantidad_real

    # Retorna 0 si nunca en la historia se ha comprado
    return 0.0



def calcular_costo_produccion(receta_id, presentacion_id):
    receta = Receta.query.get(receta_id)
    presentacion = Presentacion.query.get(presentacion_id)

    if not receta or not presentacion:
        return 0.0

    costo_total_liquido = 0.0

    # 1. Calcular el costo del líquido basado en la explosión de materiales
    for detalle in receta.detalles:
        # Calcular cuántos ml de este componente se necesitan
        ml_requeridos = (detalle.porcentaje / 100) * presentacion.mililitros

        # Obtener el costo por ml de esta materia prima
        costo_promedio_ml = obtener_costo_promedio_insumo(detalle.materia_prima_id, tipo_item='materia')

        costo_total_liquido += (ml_requeridos * costo_promedio_ml)

    # 2. Obtener el costo del envase (el bote de la presentación)
    costo_envase = obtener_costo_promedio_insumo(presentacion.id, tipo_item='presentacion')

    # Costo final: Líquido + Envase
    costo_final = costo_total_liquido + costo_envase
    
    return round(costo_final, 2)