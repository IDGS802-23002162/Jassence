from models import DetalleReceta, LogAuditoria, db, Receta
from . import formulas_bp
from flask import render_template, request, redirect, url_for, flash


# ==========================================
# LOG DE AUDITORÍA
# ==========================================
def crear_log(accion, tabla, registro_id, detalle, usuario_id=None):
    log = LogAuditoria(
        usuario_id=usuario_id,
        accion=accion,
        tabla_afectada=tabla,
        registro_id=registro_id,
        detalle=detalle
    )
    db.session.add(log)


# ==========================================
# LISTA DE FÓRMULAS
# ==========================================
@formulas_bp.route('/explosion-materiales')
def index_formulas():
    recetas = Receta.query.all()

    return render_template('modulos_front/formulas/formulas.html',
        titulo="Gestión de Fórmulas",
        recetas=recetas
    )


# ==========================================
# NUEVA FÓRMULA
# ==========================================
@formulas_bp.route('/formulas/nueva', methods=['GET', 'POST'])
def nueva_formula():
    if request.method == 'POST':
        nombre = request.form.get('nombre_perfume')
        inspiracion = request.form.get('inspiracion')
        descripcion = request.form.get('descripcion')

        esencia = float(request.form.get('esencia'))
        etanol = float(request.form.get('etanol'))
        fijador = float(request.form.get('fijador'))

        # VALIDACIÓN
        if round(esencia, 2) != 40 or round(etanol, 2) != 55 or round(fijador, 2) != 5:
            flash("La fórmula debe ser 40% esencia, 55% etanol y 5% fijador", "error")
            return redirect(url_for('formulas.nueva_formula'))

        nueva = Receta(
            nombre_perfume=nombre,
            inspiracion=inspiracion,
            descripcion=descripcion
        )

        db.session.add(nueva)
        db.session.flush()  # Para obtener el ID antes del commit final

        # DETALLES
        d1 = DetalleReceta(receta_id=nueva.id, porcentaje=esencia, tipo_componente='esencia')
        d2 = DetalleReceta(receta_id=nueva.id, porcentaje=etanol, tipo_componente='etanol')
        d3 = DetalleReceta(receta_id=nueva.id, porcentaje=fijador, tipo_componente='fijador')

        db.session.add_all([d1, d2, d3])

        # REGISTRO EN AUDITORÍA
        crear_log(
            accion="CREATE",
            tabla="Recetas",
            registro_id=nueva.id,
            detalle=f"Receta creada: {nueva.nombre_perfume} (ID: {nueva.id})"
        )

        db.session.commit()

        flash("Fórmula creada correctamente", "success")
        return redirect(url_for('formulas.index_formulas'))

    return render_template('modulos_front/formulas/nueva_formula.html')


# ==========================================
# DETALLE
# ==========================================
@formulas_bp.route('/formulas/detalles/<int:id>')
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
                "porcentaje": d.porcentaje,
                "ml": round(ml, 2)
            })

    return render_template('modulos_front/formulas/detalles.html',
        receta=receta,
        detalles=detalles,
        calculos=calculos
    )


# ==========================================
# MODIFICAR
# ==========================================
@formulas_bp.route('/formulas/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_formula(id):
    receta = Receta.query.get_or_404(id)
    detalles = DetalleReceta.query.filter_by(receta_id=id).all()

    if request.method == 'POST':
        receta.nombre_perfume = request.form.get('nombre_perfume')
        receta.inspiracion = request.form.get('inspiracion')
        receta.descripcion = request.form.get('descripcion')
        receta.genero = request.form.get('genero')
        receta.ocasion = request.form.get('ocasion')
        receta.familia_olfativa = request.form.get('familia_olfativa')
        receta.imagen_url = request.form.get('imagen_url')
        
        try:
            esencia_base = float(request.form.get('esencia_base', 0))
            etanol = float(request.form.get('etanol', 0))
            fijador = float(request.form.get('fijador', 0))
            
            nombres_extras = request.form.getlist('nombres_esencias[]')
            porcentajes_extras = request.form.getlist('porcentajes_esencias[]')
            
            suma_total = esencia_base + etanol + fijador
            extras_lista = []
            
            for i in range(len(nombres_extras)):
                nombre_limpio = nombres_extras[i].strip()
                if nombre_limpio:
                    p = float(porcentajes_extras[i] or 0)
                    suma_total += p
                    extras_lista.append({'nombre': nombre_limpio, 'porcentaje': p})

            if abs(suma_total - 100) > 0.01:
                flash(f"Error: La suma es {suma_total}%. Debe ser 100%.", "error")
                return redirect(url_for('formulas.modificar_formula', id=id))

            # RECONSTRUIR DETALLES
            DetalleReceta.query.filter_by(receta_id=id).delete()

            fijos = [('esencia_base', esencia_base), ('etanol', etanol), ('fijador', fijador)]
            for tipo, valor in fijos:
                db.session.add(DetalleReceta(receta_id=id, tipo_componente=tipo, porcentaje=valor))

            for extra in extras_lista:
                db.session.add(DetalleReceta(receta_id=id, tipo_componente=extra['nombre'], porcentaje=extra['porcentaje']))

            # REGISTRO EN AUDITORÍA
            crear_log(
                accion="UPDATE",
                tabla="Recetas",
                registro_id=id,
                detalle=f"Fórmula recalibrada y datos actualizados para: {receta.nombre_perfume}"
            )

            db.session.commit()
            flash("Fórmula y datos de marketing actualizados", "success")
            return redirect(url_for('formulas.index_formulas'))

        except ValueError:
            flash("Error: Los porcentajes deben ser números válidos.", "error")
            return redirect(url_for('formulas.modificar_formula', id=id))

    esencia = next((d.porcentaje for d in detalles if d.tipo_componente == 'esencia_base'), 0)
    etanol = next((d.porcentaje for d in detalles if d.tipo_componente == 'etanol'), 0)
    fijador = next((d.porcentaje for d in detalles if d.tipo_componente == 'fijador'), 0)

    return render_template('modulos_front/formulas/modificar.html', 
            receta=receta, esencia=esencia, etanol=etanol, fijador=fijador)


# ==========================================
# ELIMINAR (SEGURO)
# ==========================================
@formulas_bp.route('/formulas/eliminar/<int:id>', methods=['POST'])
def eliminar_formula(id):
    receta = Receta.query.get_or_404(id)
    nombre_borrado = receta.nombre_perfume

    DetalleReceta.query.filter_by(receta_id=id).delete()
    db.session.delete(receta)

    # REGISTRO EN AUDITORÍA
    crear_log(
        accion="DELETE",
        tabla="Recetas",
        registro_id=id,
        detalle=f"Receta eliminada: {nombre_borrado} (ID: {id})"
    )

    db.session.commit()

    flash("Fórmula eliminada", "success")
    return redirect(url_for('formulas.index_formulas'))