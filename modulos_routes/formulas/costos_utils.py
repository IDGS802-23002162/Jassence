from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, Compra, DetalleCompra, Receta, Presentacion

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