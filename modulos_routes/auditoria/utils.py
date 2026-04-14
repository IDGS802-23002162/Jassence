from models import db, LogAuditoria
from flask_security import current_user
from datetime import datetime

def registrar_log(accion, tabla, registro_id, detalle):
    # Verificamos si hay un usuario en sesión, de lo contrario registramos None (Ej. intentos fallidos)
    user_id = current_user.id if current_user.is_authenticated else None
    
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

# COMPARAR CAMBIOS (EXCLUSIVO FORMULAS)

def generar_detalle_cambios_formula(receta_antigua, detalles_antiguos, form_data, nueva_imagen_url, nuevos_ingredientes_dict):
    cambios = []

    # 1. Comparar campos de texto básicos
    campos_texto = {
        'nombre_perfume': 'Nombre',
        'inspiracion': 'Inspiración',
        'descripcion': 'Descripción',
        'genero': 'Género',
        'ocasion': 'Ocasión',
        'familia_olfativa': 'Familia Olfativa'
    }

    for campo, etiqueta in campos_texto.items():
        valor_antiguo = str(getattr(receta_antigua, campo) or '').strip()
        valor_nuevo = str(form_data.get(campo) or '').strip()
        if valor_antiguo != valor_nuevo:
            cambios.append(f"{etiqueta}: '{valor_antiguo}' -> '{valor_nuevo}'")

    # 2. Comparar la imagen
    if nueva_imagen_url and receta_antigua.imagen_url != nueva_imagen_url:
        cambios.append(f"Imagen actualizada a '{nueva_imagen_url}'")

    # 3. Comparar ingredientes (DetalleReceta)
    ingredientes_antiguos_dict = {
        d.materia_prima_id: {'nombre': d.materia_prima.nombre, 'porcentaje': float(d.porcentaje)}
        for d in detalles_antiguos
    }

    cambios_ingredientes = []
    # Unimos los IDs de los ingredientes viejos y los nuevos para iterar sobre todos
    todas_las_keys = set(ingredientes_antiguos_dict.keys()).union(set(nuevos_ingredientes_dict.keys()))

    for mp_id in todas_las_keys:
        antiguo = ingredientes_antiguos_dict.get(mp_id)
        nuevo = nuevos_ingredientes_dict.get(mp_id)

        if antiguo and not nuevo:
            cambios_ingredientes.append(f"Eliminó: {antiguo['nombre']}")
        elif nuevo and not antiguo:
            cambios_ingredientes.append(f"Agregó: {nuevo['nombre']} ({nuevo['porcentaje']}%)")
        elif antiguo and nuevo and antiguo['porcentaje'] != nuevo['porcentaje']:
            cambios_ingredientes.append(f"{antiguo['nombre']}: {antiguo['porcentaje']}% -> {nuevo['porcentaje']}%")

    if cambios_ingredientes:
        cambios.append("Ingredientes [ " + ", ".join(cambios_ingredientes) + " ]")

    # Si hubo cambios los une con un separador, si no, devuelve un string por defecto
    return " | ".join(cambios) if cambios else "Actualización sin cambios detectables."

# CHEQUEO CANTIDADES PRODUCCION

def generar_resumen_consumo_produccion(orden):
    if not orden.receta or not orden.cantidad_producir:
        return "Sin consumo registrado"

    cantidad_producida = orden.cantidad_producir
    detalles_consumo = []

    for detalle in orden.receta.detalles:
        cantidad_usada = (detalle.porcentaje / 100) * cantidad_producida
        nombre_mp = detalle.materia_prima.nombre if detalle.materia_prima else "MP Desconocida"
        detalles_consumo.append(f"{cantidad_usada:.2f} de {nombre_mp}")

    return ", ".join(detalles_consumo)

def generar_detalle_entrada_producto(orden):
    nombre_receta = orden.receta.nombre_perfume if orden.receta else "Desconocido"
    presentacion = ""
    
    if orden.producto_terminado and orden.producto_terminado.presentacion:
        presentacion = f"{orden.producto_terminado.presentacion.nombre} {orden.producto_terminado.presentacion.mililitros}ml"
        
    return f"Entrada a stock por Orden #{orden.id}: +{orden.cantidad_producir} de {nombre_receta} {presentacion}"