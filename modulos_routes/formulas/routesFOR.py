from models import DetalleReceta, LogAuditoria, db, Receta, MateriaPrima, Presentacion, ProductoTerminado
from . import formulas_bp
from flask import render_template, request, redirect, url_for, flash
from flask_security import roles_accepted
from modulos_routes.auditoria.utils import registrar_log, generar_detalle_cambios_formula
from sqlalchemy.exc import IntegrityError 
import json
from modulos_routes.formulas.costos_utils import obtener_costo_promedio_insumo



# ==========================================
# LISTA DE FÓRMULAS
# ==========================================
@formulas_bp.route('/explosion-materiales')
@roles_accepted('admin' , 'produccion')
def index_formulas():
    recetas = Receta.query.all()

    return render_template('modulos_front/formulas/formulas.html',
        titulo="Gestión de Fórmulas",
        recetas=recetas
    )

# ==========================================
# CREAR NUEVA FÓRMULA  
# ==========================================

@formulas_bp.route('/formulas/nueva', methods=['GET', 'POST'])
@roles_accepted('admin', 'produccion')
def nueva_formula():
    if request.method == 'POST':
        nombre = request.form.get('nombre_perfume')
        inspiracion = request.form.get('inspiracion')
        descripcion = request.form.get('descripcion')
        genero = request.form.get('genero')
        ocasion = request.form.get('ocasion')
        familia_olfativa = request.form.get('familia_olfativa')

        try:
            file = request.files.get('imagen')
            imagen_nombre = None
            if file and file.filename.strip() != "":
                from werkzeug.utils import secure_filename
                import os
                filename = secure_filename(file.filename)
                carpeta = 'static/img/productos'
                os.makedirs(carpeta, exist_ok=True)
                ruta = os.path.join(carpeta, filename)
                file.save(ruta)
                imagen_nombre = filename

            esencia_id = int(request.form.get('esencia_base_nombre', 0))
            alcohol_id = int(request.form.get('alcohol_nombre', 0))
            fijador_id = int(request.form.get('fijador_nombre', 0))

            esencia_base = float(request.form.get('esencia_base') or 0)
            alcohol = float(request.form.get('alcohol') or 0)
            fijador = float(request.form.get('fijador') or 0)

            extras_ids = request.form.getlist('nombres_esencias[]')
            porcentajes_extras = request.form.getlist('porcentajes_esencias[]')

            suma_total = esencia_base + alcohol + fijador
            extras_lista = []
            for i in range(len(extras_ids)):
                if extras_ids[i]:
                    mp_id = int(extras_ids[i])
                    p = float(porcentajes_extras[i] or 0)
                    suma_total += p
                    extras_lista.append({'id': mp_id, 'porcentaje': p})

            if abs(suma_total - 100) > 0.01:
                flash(f"Error: La suma es {suma_total}%. Debe ser 100%.", "error")
                return redirect(url_for('formulas.nueva_formula'))

            nueva = Receta(
                nombre_perfume=nombre,
                inspiracion=inspiracion,
                descripcion=descripcion,
                genero=genero,
                ocasion=ocasion,
                familia_olfativa=familia_olfativa,
                imagen_url=imagen_nombre
            )
            db.session.add(nueva)
            db.session.flush()  

            for mp_id, valor, tipo in [
                (esencia_id, esencia_base, 'esencia'),
                (alcohol_id, alcohol, 'alcohol'),
                (fijador_id, fijador, 'fijador')
            ]:
                if mp_id and valor > 0:
                    db.session.add(DetalleReceta(
                        receta_id=nueva.id,
                        materia_prima_id=mp_id,
                        porcentaje=valor,
                        tipo_componente=tipo
                    ))

            for extra in extras_lista:
                if extra['porcentaje'] > 0:
                    mp = MateriaPrima.query.get(extra['id'])
                    db.session.add(DetalleReceta(
                        receta_id=nueva.id,
                        materia_prima_id=extra['id'],
                        porcentaje=extra['porcentaje'],
                        tipo_componente=mp.tipo
                    ))

            # ==========================================
            # NUEVO: CREACIÓN DE PRODUCTOS TERMINADOS
            # ==========================================
            presentaciones = Presentacion.query.all()
            for pres in presentaciones:
                # Buscamos el input dinámico generado en el HTML
                precio_input = request.form.get(f'precio_presentacion_{pres.id}')
                
                # Si el usuario le puso precio, creamos el producto terminado
                if precio_input and float(precio_input) > 0:
                    nuevo_producto = ProductoTerminado(
                        receta_id=nueva.id,
                        presentacion_id=pres.id,
                        stock_disponible_venta=0,  # Empieza en 0 porque apenas es la receta
                        stock_minimo=5,            # Puedes ajustar tu stock mínimo por defecto
                        precio_venta=float(precio_input),
                        estado='activo',
                        stock_comprometido=0
                    )
                    db.session.add(nuevo_producto)

            registrar_log(
                accion="CREATE",
                tabla="recetas",
                registro_id=nueva.id,
                detalle=f"Nueva fórmula creada: {nombre}"
            )
            db.session.commit()
            flash("Fórmula creada correctamente", "success")
            return redirect(url_for('formulas.index_formulas'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar la fórmula: {str(e)}", "error")
            return redirect(url_for('formulas.nueva_formula'))

    # 1. Generar diccionario de costos de materias primas {id: costo_por_ml}
    materias_primas = MateriaPrima.query.all()
    costos_mp = {}
    for mp in materias_primas:
        costos_mp[mp.id] = obtener_costo_promedio_insumo(mp.id, tipo_item='materia')

    # 2. Generar diccionario de costos de envases {id: costo_envase}
    presentaciones_bd = Presentacion.query.all()
    costos_envases = {}
    info_presentaciones = {} # Para saber los ml de cada una en JS
    for p in presentaciones_bd:
        costos_envases[p.id] = obtener_costo_promedio_insumo(p.id, tipo_item='presentacion')
        info_presentaciones[p.id] = p.mililitros

    return render_template(
        'modulos_front/formulas/nueva_formula.html',
        esencias=MateriaPrima.query.filter_by(tipo='esencia').all(),
        alcohol_lista=MateriaPrima.query.filter_by(tipo='alcohol').all(),
        fijadores=MateriaPrima.query.filter_by(tipo='fijador').all(),
        presentaciones=Presentacion.query.all(),

        costos_mp_json=json.dumps(costos_mp),
        costos_envases_json=json.dumps(costos_envases),
        info_presentaciones_json=json.dumps(info_presentaciones)
    )

# ==========================================
# DETALLE
# ==========================================
@formulas_bp.route('/formulas/detalles/<int:id>')
@roles_accepted('admin', 'produccion')
def detalle_formula(id):
    receta = Receta.query.get_or_404(id)
    detalles = DetalleReceta.query.filter_by(receta_id=id).all()

    presentaciones = [30, 50, 100]
    calculos = {}

    for p in presentaciones:
        calculos[p] = []
        for d in detalles:
            ml = (d.porcentaje / 100) * p
            calculos[p].append({
                "tipo": d.tipo_componente,
                "materia": d.materia_prima.nombre,
                "porcentaje": d.porcentaje,
                "ml": round(ml, 2)
            })

    return render_template(
        'modulos_front/formulas/detalles.html',
        receta=receta,
        detalles=detalles,
        calculos=calculos
    )


# ==========================================
# MODIFICAR FÓRMULA
# ==========================================
@formulas_bp.route('/formulas/modificar/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'produccion')
def modificar_formula(id):
    receta = Receta.query.get_or_404(id)
    detalles = DetalleReceta.query.filter_by(receta_id=id).all()

    if request.method == 'POST':
        # 🔥 LOG DINÁMICO: Inicializar lista de cambios y comparar campos generales
        cambios = []
        campos_texto = ['nombre_perfume', 'inspiracion', 'descripcion', 'genero', 'ocasion', 'familia_olfativa']
        
        for campo in campos_texto:
            valor_viejo = str(getattr(receta, campo) or '').strip()
            valor_nuevo = str(request.form.get(campo) or '').strip()
            
            if valor_viejo != valor_nuevo:
                cambios.append(f"{campo.replace('_', ' ').capitalize()}: '{valor_viejo}' -> '{valor_nuevo}'")
            
            setattr(receta, campo, request.form.get(campo))

        try:
            # IMAGEN
            file = request.files.get('imagen')  
            if file and file.filename.strip() != "":
                from werkzeug.utils import secure_filename
                import os

                filename = secure_filename(file.filename)
                carpeta = 'static/img/productos'
                os.makedirs(carpeta, exist_ok=True)
                ruta = os.path.join(carpeta, filename)

                try:
                    file.save(ruta)
                    receta.imagen_url = filename
                    cambios.append("Imagen actualizada") # 🔥 LOG DINÁMICO
                    print(f"[INFO] Imagen guardada correctamente en: {ruta}")
                except Exception as e:
                    flash(f"Error al guardar imagen: {str(e)}", "error")
                    print(f"[ERROR] Falló guardado de imagen: {str(e)}")

            # Componentes principales
            esencia_id = int(request.form.get('esencia_base_nombre', 0))
            alcohol_id = int(request.form.get('alcohol_nombre', 0))
            fijador_id = int(request.form.get('fijador_nombre', 0))

            esencia_base = float(request.form.get('esencia_base') or 0)
            alcohol = float(request.form.get('alcohol') or 0)
            fijador = float(request.form.get('fijador') or 0)

            # Extras
            extras_ids = request.form.getlist('nombres_esencias[]')
            porcentajes_extras = request.form.getlist('porcentajes_esencias[]')

            suma_total = esencia_base + alcohol + fijador
            extras_lista = []

            for i in range(len(extras_ids)):
                if extras_ids[i]:
                    mp_id = int(extras_ids[i])
                    p = float(porcentajes_extras[i] or 0)
                    suma_total += p
                    extras_lista.append({'id': mp_id, 'porcentaje': p})

            # Validar suma 100%
            if abs(suma_total - 100) > 0.01:
                flash(f"Error: La suma es {suma_total}%. Debe ser 100%.", "error")
                return redirect(url_for('formulas.modificar_formula', id=id))

            # 🔥 LOG DINÁMICO: Comparar Ingredientes (Detalles) antes de borrarlos
            detalles_viejos = {d.materia_prima_id: d.porcentaje for d in detalles}
            
            detalles_nuevos = {}
            if esencia_id: detalles_nuevos[esencia_id] = esencia_base
            if alcohol_id: detalles_nuevos[alcohol_id] = alcohol
            if fijador_id: detalles_nuevos[fijador_id] = fijador
            for ex in extras_lista: detalles_nuevos[ex['id']] = ex['porcentaje']

            for mp_id, porc_nuevo in detalles_nuevos.items():
                if mp_id not in detalles_viejos:
                    cambios.append(f"Agregó MP {mp_id} ({porc_nuevo}%)")
                elif float(detalles_viejos[mp_id]) != float(porc_nuevo):
                    cambios.append(f"Modificó % MP {mp_id}: {detalles_viejos[mp_id]}% -> {porc_nuevo}%")
            
            for mp_id in detalles_viejos:
                if mp_id not in detalles_nuevos:
                    cambios.append(f"Eliminó MP {mp_id}")

            # Eliminar detalles existentes
            DetalleReceta.query.filter_by(receta_id=id).delete()

            # Guardar componentes principales
            for mp_id, valor, tipo in [
                (esencia_id, esencia_base, 'esencia'),
                (alcohol_id, alcohol, 'alcohol'),
                (fijador_id, fijador, 'fijador')
            ]:
                if mp_id and valor > 0:
                    db.session.add(DetalleReceta(
                        receta_id=id,
                        materia_prima_id=mp_id,
                        porcentaje=valor,
                        tipo_componente=tipo
                    ))

            # Guardar extras
            for extra in extras_lista:
                if extra['porcentaje'] > 0:
                    mp = MateriaPrima.query.get(extra['id'])
                    db.session.add(DetalleReceta(
                        receta_id=id,
                        materia_prima_id=extra['id'],
                        porcentaje=extra['porcentaje'],
                        tipo_componente=mp.tipo 
                    ))

            # =======================================================
            # 🔥 ACTUALIZACIÓN DE PRECIOS Y LOG DINÁMICO
            # =======================================================
            productos_existentes = ProductoTerminado.query.filter_by(receta_id=id).all()

            for producto in productos_existentes:
                pres_id = producto.presentacion_id
                precio_input = request.form.get(f'precio_presentacion_{pres_id}')
                
                if precio_input and precio_input.strip() != "":
                    nuevo_precio = float(precio_input)
                    precio_actual = float(producto.precio_venta or 0)
                    
                    if precio_actual != nuevo_precio:
                        cambios.append(f"Precio (Pres. {pres_id}): ${precio_actual} -> ${nuevo_precio}")
                        producto.precio_venta = nuevo_precio
            # =======================================================

            # 🔥 LOG DINÁMICO: Consolidar y registrar el Log
            if cambios:
                texto_cambios = " | ".join(cambios)
                detalle_log = f"Modificaciones: {texto_cambios}"
            else:
                detalle_log = f"Fórmula guardada sin cambios detectados."

            registrar_log(
                accion="UPDATE",
                tabla="recetas",
                registro_id=id,
                detalle=detalle_log
            )

            db.session.commit()
            flash("Fórmula y precios actualizados correctamente", "success")
            return redirect(url_for('formulas.index_formulas'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "error")
            return redirect(url_for('formulas.modificar_formula', id=id))

    detalles_por_tipo = {d.tipo_componente: d for d in detalles}

    esencia_det = detalles_por_tipo.get('esencia', None)
    alcohol_det = detalles_por_tipo.get('alcohol', None)
    fijador_det = detalles_por_tipo.get('fijador', None)

    # IDs de los componentes principales
    ids_fijos = set()
    for tipo in ['esencia', 'alcohol', 'fijador']:
        # toma solo el primero de cada tipo como fijo
        det = next((d for d in detalles if d.tipo_componente == tipo), None)
        if det:
            ids_fijos.add(det.id)

    # Detalles dinámicos: todo lo demás
    detalles_dinamicos = [d for d in detalles if d.id not in ids_fijos]

    # Asignar los fijos correctamente
    esencia_det = next((d for d in detalles if d.id in ids_fijos and d.tipo_componente=='esencia'), None)
    alcohol_det = next((d for d in detalles if d.id in ids_fijos and d.tipo_componente=='alcohol'), None)
    fijador_det = next((d for d in detalles if d.id in ids_fijos and d.tipo_componente=='fijador'), None)
    precios_actuales = {prod.presentacion_id: prod.precio_venta for prod in receta.productos_terminados}

    return render_template(
        'modulos_front/formulas/modificar.html',
        receta=receta,
        esencia=esencia_det.porcentaje if esencia_det else 0,
        alcohol=alcohol_det.porcentaje if alcohol_det else 0,
        fijador=fijador_det.porcentaje if fijador_det else 0,
        esencia_nombre=esencia_det.materia_prima_id if esencia_det else None,
        alcohol_nombre=alcohol_det.materia_prima_id if alcohol_det else None,
        fijador_nombre=fijador_det.materia_prima_id if fijador_det else None,
        detalles_dinamicos=detalles_dinamicos,
        esencias=MateriaPrima.query.filter_by(tipo='esencia').all(),
        alcohol_lista=MateriaPrima.query.filter_by(tipo='alcohol').all(),
        fijadores=MateriaPrima.query.filter_by(tipo='fijador').all(),
        presentaciones=Presentacion.query.all(),
        precios_actuales=precios_actuales
    ) 


# ==========================================
# ACTIVAR / DESACTIVAR FÓRMULA (BAJA LÓGICA)
# ==========================================
@formulas_bp.route('/formulas/toggle_estado/<int:id>', methods=['POST'])
@roles_accepted('admin', 'produccion')
def toggle_estado_formula(id):
    receta = Receta.query.get_or_404(id)
    nombre_perfume = receta.nombre_perfume

    try:
        if receta.activo:
            # Si está activa -> LA DESACTIVAMOS
            receta.activo = False
            for producto in receta.productos_terminados:
                producto.estado = 'Inactivo'
                
            accion_log = "DELETE"
            detalle_log = f"Fórmula inhabilitada (Baja Lógica): {nombre_perfume} (ID: {id})"
            mensaje_flash = "Fórmula desactivada correctamente."
        else:
            # Si está inactiva -> LA REACTIVAMOS
            receta.activo = True
            for producto in receta.productos_terminados:
                producto.estado = 'Activo'
                
            accion_log = "UPDATE"
            detalle_log = f"Fórmula reactivada: {nombre_perfume} (ID: {id})"
            mensaje_flash = "Fórmula reactivada y lista para usarse."

        registrar_log(
            accion=accion_log,
            tabla="recetas",
            registro_id=id,
            detalle=detalle_log
        )

        db.session.commit()
        flash(mensaje_flash, "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error inesperado al cambiar el estado: {str(e)}", "error")

    return redirect(url_for('formulas.index_formulas'))
    