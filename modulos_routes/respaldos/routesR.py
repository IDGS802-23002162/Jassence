import os
import subprocess
import tempfile
import random
import threading
import re
from datetime import datetime
from functools import wraps
from flask import (
    Blueprint, send_file, send_from_directory, jsonify, 
    request, current_app, render_template, session, 
    redirect, url_for, flash
)
from flask_security import roles_required, current_user
from flask_mailman import EmailMessage
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
from modulos_routes.auditoria.utils import registrar_log

# Importamos el blueprint y la instancia de mail
from . import respaldos_bp


# Directorio para los respaldos automatizados
BACKUP_DIR = os.path.join(os.getcwd(), 'backups_automatizados')
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# ==========================================
# CANDADO 2FA
# ==========================================
def requiere_2fa_step_up(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si no tiene la llave, lo mandamos a pedirla
        if not session.get('modulo_respaldos_desbloqueado'):
            session['next_url'] = request.url
            return redirect(url_for('respaldos.pedir_codigo_2fa')) 
        return f(*args, **kwargs)
    return decorated_function

@respaldos_bp.route('/admin/backups/salir-seguro')
@roles_required('admin')
def salir_seguro():
    session.pop('modulo_respaldos_desbloqueado', None)
    session.pop('codigo_esperado_respaldos', None)
    flash('Módulo de respaldos bloqueado.', 'info')
    return redirect(url_for('index'))


# ==========================================
# RUTAS DEL PANEL Y OPERACIONES
# ==========================================

@respaldos_bp.route('/admin/backups', methods=['GET'])
@roles_required('admin')
@requiere_2fa_step_up
def panel_respaldos():
    archivos_sql = []
    if os.path.exists(BACKUP_DIR):
        archivos = os.listdir(BACKUP_DIR)
        archivos_sql = [f for f in archivos if f.endswith('.sql')]
        archivos_sql.sort(reverse=True)

    registrar_log(
            accion='RESPALDOS',
            tabla='accesos',
            registro_id=current_user.id,
            detalle='Accedio a respaldos'
        )
        
    return render_template('modulos_front/respaldos/respaldos.html', backups_disponibles=archivos_sql)


@respaldos_bp.route('/api/admin/backup/download', methods=['GET'])
@roles_required('admin')
@requiere_2fa_step_up
def descargar_respaldo():
    try:
        db_host = current_app.config.get('MYSQL_HOST', 'localhost')
        db_user = current_app.config.get('MYSQL_USER', 'jassence_backup')
        db_pass = current_app.config.get('MYSQL_PASSWORD', 'jassence_backup_password_$')
        db_name = current_app.config.get('MYSQL_DB', 'jassencebd')

        fd, temp_path = tempfile.mkstemp(suffix='.sql')
        os.close(fd)
        
        ruta_mysqldump = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
        
        comando = [
            ruta_mysqldump,
            f'-h{db_host}',
            f'-u{db_user}',
            f'-p{db_pass}',
            '--single-transaction',
            '--routines',
            '--triggers',
            '--no-tablespaces',
            db_name
        ]
        
        with open(temp_path, 'w') as f:
            subprocess.run(comando, stdout=f, check=True)

        fecha_actual = datetime.now().strftime('%d_%m_%Y_%H%M')
        nombre_archivo = f"respaldo_jassence_{fecha_actual}.sql"

        registrar_log(
            accion='RESPALDOS',
            tabla='accesos',
            registro_id=current_user.id,
            detalle='Genero un respaldo nuevo '
        )
        
        fecha_actual = datetime.now().strftime('%d_%m_%Y_%H%M')
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/sql'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@respaldos_bp.route('/api/admin/backup/restore', methods=['POST'])
@roles_required('admin')
@requiere_2fa_step_up
def restaurar_respaldo():
    if 'backup_file' not in request.files:
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400
        
    archivo = request.files['backup_file']
    if archivo.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    try:
        db_host = current_app.config.get('MYSQL_HOST', 'localhost')
        db_user = current_app.config.get('MYSQL_USER', 'jassence_backup')
        db_pass = current_app.config.get('MYSQL_PASSWORD', 'jassence_backup_password_$')
        db_name = current_app.config.get('MYSQL_DB', 'jassencebd')

        nombre_seguro = secure_filename(archivo.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, nombre_seguro)
        archivo.save(temp_path)

        # ==========================================
        # NUEVO: LIMPIEZA DE PRIVILEGIOS (DEFINER)
        # ==========================================
        import re  # (Preferiblemente mueve esto al inicio de tu app.py)
        
        # 1. Leer el archivo que acabamos de guardar
        with open(temp_path, 'r', encoding='utf-8') as f:
            contenido_sql = f.read()

        # 2. Eliminar cláusulas DEFINER (convierte a jassence_backup en el dueño)
        contenido_sql = re.sub(r'DEFINER\s*=\s*`[^`]+`@`[^`]+`', '', contenido_sql)
        contenido_sql = re.sub(r'/\*!50013 DEFINER\s*=\s*.*?\*/', '', contenido_sql)

        # 3. Sobreescribir el archivo temporal ya limpio
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(contenido_sql)
        # ==========================================

        ruta_mysql = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
        
        # 1. Definimos el comando como LISTA, SIN el símbolo "<"
        comando = [
            ruta_mysql,
            f'-h{db_host}',
            f'-u{db_user}',
            f'-p{db_pass}',
            db_name
        ]

        # 2. PREVENCIÓN DE DEADLOCK
        from models import db 
        db.session.remove()
        db.engine.dispose()

        # 3. Le damos el archivo a MySQL directamente desde Python
        with open(temp_path, 'r', encoding='utf-8') as f:
            resultado = subprocess.run(
                comando,
                stdin=f,             # Inyectamos el archivo limpio
                capture_output=True, # Atrapamos cualquier error real
                text=True,
                check=False
            )
        
        os.remove(temp_path)

        # 4. Revisamos si hubo algún error en MySQL (ignora el Warning de la contraseña)
        if resultado.returncode != 0:
            print("--- ERROR DE MYSQL ---")
            print(resultado.stderr) 
            return jsonify({"error": "Error interno en MySQL. Revisa la consola de Flask."}), 500

        # Si llegamos aquí, ¡funcionó! Ya podemos guardar el log tranquilamente
        registrar_log(
             accion='RESPALDOS',
             tabla='accesos',
             registro_id=current_user.id,
             detalle=f'Restauró la base de datos usando el archivo: {nombre_seguro}'
        )
        
        return jsonify({"mensaje": "Base de datos restaurada con éxito"}), 200

    except Exception as e:
        print(f"Excepción: {str(e)}")
        return jsonify({"error": f"Error en restauración: {str(e)}"}), 500


@respaldos_bp.route('/api/admin/backup/auto/download/<nombre_archivo>', methods=['GET'])
@roles_required('admin')
@requiere_2fa_step_up
def descargar_desde_servidor(nombre_archivo):
    try:
        nombre_seguro = secure_filename(nombre_archivo)

        registrar_log(
            accion='RESPALDOS',
            tabla='accesos',
            registro_id=current_user.id,
            detalle=f'Descargó respaldo automático: {nombre_seguro}'
        )

        return send_from_directory(
            directory=BACKUP_DIR,
            path=nombre_seguro,
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({"error": "El archivo de respaldo no existe"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# GESTIÓN DE 2FA PERSONALIZADO
# ==========================================

def enviar_mail_async(app, msg):
    # Usamos el contexto de la app para que Mailman encuentre la configuración
    with app.app_context():
        try:
            msg.send()
            print(f"[{datetime.now()}] Correo enviado exitosamente vía hilo.")
        except Exception as e:
            print(f"[{datetime.now()}] Error en envío asíncrono: {e}")

@respaldos_bp.route('/admin/backups/verificar-seguridad', methods=['GET', 'POST'])
@roles_required('admin')
def pedir_codigo_2fa():
    # 1. SI ES POST: Validar el código
    if request.method == 'POST':
        codigo_ingresado = request.form.get('codigo_2fa')
        codigo_esperado = session.get('codigo_esperado_respaldos')

        if codigo_ingresado and codigo_ingresado == codigo_esperado:
            session.pop('codigo_esperado_respaldos', None)
            session['modulo_respaldos_desbloqueado'] = True
            siguiente = session.pop('next_url', url_for('respaldos.panel_respaldos'))
            return redirect(siguiente)
        else:
            flash('Código incorrecto. Intenta de nuevo.', 'error')
            return render_template('modulos_front/respaldos/verificar_2fa.html')

    # 2. SI ES GET: Generar y enviar código
    # Si ya hay uno en sesión, no generamos otro para evitar spam al refrescar
    if 'codigo_esperado_respaldos' in session:
        print(f"[{datetime.now()}] Usando código existente en sesión.")
        return render_template('modulos_front/respaldos/verificar_2fa.html')

    codigo = str(random.randint(100000, 999999))
    session['codigo_esperado_respaldos'] = codigo
    
    # IMPORTANTE: Generamos el mensaje ANTES de lanzar el hilo
    try:
        html_content = render_template('modulos_front/respaldos/email_2fa_respaldos.html', token=codigo)
        
        msg = EmailMessage(
            subject=" Código de Seguridad - Respaldos Jassence",
            body=html_content,
            from_email=current_app.config.get('MAIL_DEFAULT_SENDER'),
            to=[current_user.email]
        )
        msg.content_subtype = "html" 
        
        # Obtenemos la instancia real de la app
        app_para_hilo = current_app._get_current_object()
        
        threading.Thread(target=enviar_mail_async, args=(app_para_hilo, msg)).start()
        
    except Exception as e:
        print(f" Error al preparar correo: {e}")

    return render_template('modulos_front/respaldos/verificar_2fa.html')
# ==========================================
# TAREA AUTOMÁTICA (SCHEDULER)
# ==========================================

def tarea_respaldo_diario():
    db_host = 'localhost'
    db_user = 'jassence_backup'
    db_pass = 'jassence_backup_password_$'
    db_name = 'jassencebd'
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"jassence_auto_{timestamp}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)
    
    ruta_mysqldump = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
    
    comando = [
        ruta_mysqldump,
        f'-h{db_host}',
        f'-u{db_user}',
        f'-p{db_pass}',
        '--single-transaction',
        '--routines',
        '--triggers',
        '--no-tablespaces',
        db_name
    ]
    
    try:
        with open(filepath, 'w') as f:
            subprocess.run(comando, stdout=f, check=True)
            registrar_log(
                accion='RESPALDOS',
                tabla='accesos',
                registro_id=None,
                detalle=f'SISTEMA: Respaldo automático diario generado con éxito -> {filename}'
            )
        print(f"[{datetime.now()}] ÉXITO: Respaldo automático guardado -> {filename}")
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: Falló el respaldo automático -> {str(e)}")

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=tarea_respaldo_diario, trigger="cron", hour=2, minute=0)
    scheduler.start()