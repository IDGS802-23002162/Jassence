from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

# ==========================================
# SEGURIDAD (Adaptado para Flask-Security-Too)
# ==========================================

# Tabla intermedia obligatoria para relacionar Usuarios y Roles
roles_users = db.Table('roles_users',
    db.Column('usuario_id', db.Integer(), db.ForeignKey('usuarios.id')),
    db.Column('rol_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Rol(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True) # Flask-Security exige que se llame 'name'
    description = db.Column(db.String(255))      # Flask-Security exige 'description'

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # --- CAMPOS OBLIGATORIOS FLASK-SECURITY ---
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    # -------------------------------------------

    # --- NUEVO: CAMPOS OBLIGATORIOS PARA 2FA (Flask-Security) ---
    tf_primary_method = db.Column(db.String(64), nullable=True)
    tf_totp_secret = db.Column(db.String(255), nullable=True)
    tf_phone_number = db.Column(db.String(128), nullable=True)

    nombre = db.Column(db.String(150), nullable=True) 
    apellidos = db.Column(db.String(150), nullable=True) 
    telefono = db.Column(db.String(20), nullable=True)
    roles = db.relationship('Rol', secondary=roles_users, backref=db.backref('usuarios', lazy='dynamic'))

class LogAuditoria(db.Model):
    _tablename_ = 'logs_auditoria'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuario')
    accion = db.Column(db.String(50))  # CREATE, UPDATE, DELETE
    tabla_afectada = db.Column(db.String(100))
    registro_id = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    detalle = db.Column(db.Text)

# ///////////////////////////////////////
# CLIENTES 
# ///////////////////////////////////////

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship('Usuario', backref=db.backref('cliente', uselist=False))


class DireccionEntrega(db.Model):
    __tablename__ = 'direcciones_entrega'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    nombre_receptor = db.Column(db.String(100))
    telefono_contacto = db.Column(db.String(20))
    calle_numero = db.Column(db.String(200))
    colonia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100), default="León")
    estado_provincia = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    referencias = db.Column(db.Text)
    es_principal = db.Column(db.Boolean)
    estado = db.Column(db.Boolean, default=True)


class MetodoPagoCliente(db.Model):
    __tablename__ = 'metodos_pago_cliente'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    tipo_pago = db.Column(db.String(50))
    token_pasarela = db.Column(db.String(255))
    ultimos_cuatro = db.Column(db.String(4))
    marca_tarjeta = db.Column(db.String(50))
    fecha_expiracion = db.Column(db.Date)
    estado = db.Column(db.Boolean, default=True)


# ///////////////////////////////////////
# INVENTARIO 
# ///////////////////////////////////////

class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad_disponible = db.Column(db.Float)
    unidad_medida = db.Column(db.String(50))
    stock_minimo = db.Column(db.Float)
    es_contenedor = db.Column(db.Boolean, default=False)


class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    tipo_insumos = db.Column(db.String(100))


class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    archivo_factura = db.Column(db.String(255))

    estado = db.Column(db.String(50), default="pendiente")  # pendiente, pedido, entregado, cancelado


class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compras'
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), primary_key=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), primary_key=True)
    cantidad_comprada = db.Column(db.Float)
    unidad_compra = db.Column(db.String(50))
    cantidad_convertida = db.Column(db.Float)
    precio_unitario = db.Column(db.Float)


# ///////////////////////////////////////
# PRODUCCION 
# ///////////////////////////////////////

class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre_perfume = db.Column(db.String(150))
    inspiracion = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.String(255))
    genero = db.Column(db.String(50))
    ocasion = db.Column(db.String(50))
    familia_olfativa = db.Column(db.String(50))


class DetalleReceta(db.Model):
    __tablename__ = 'detalle_recetas'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    porcentaje = db.Column(db.Float)
    tipo_componente = db.Column(db.String(50))


class Presentacion(db.Model):
    __tablename__ = 'presentaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    mililitros = db.Column(db.Integer)

class ProductoTerminado(db.Model):
    _tablename_ = 'productos_terminados'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentaciones.id'))
    stock_disponible_venta = db.Column(db.Integer)
    stock_minimo = db.Column(db.Integer)
    precio_venta = db.Column(db.Float)
    estado = db.Column(db.String(50))

    receta = db.relationship('Receta')
    presentacion = db.relationship('Presentacion')


class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'

    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=True)
    producto_terminado_id = db.Column(db.Integer, db.ForeignKey('productos_terminados.id'))
    cantidad_producir = db.Column(db.Integer)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)

    estado = db.Column(db.String(50))  # pendiente, en_proceso, terminado, cancelado


# ///////////////////////////////////////
# MERMAS 
# ///////////////////////////////////////

class MermaInventario(db.Model):
    __tablename__ = 'merma_inventario'

    id = db.Column(db.Integer, primary_key=True)
    tipo_item = db.Column(db.String(50))  # materia_prima, producto_terminado
    item_id = db.Column(db.Integer)
    etapa = db.Column(db.String(50))  # produccion, almacen, etc
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    cantidad_perdida = db.Column(db.Float)
    unidad_medida = db.Column(db.String(50))

    motivo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)

    orden_produccion_id = db.Column(db.Integer, db.ForeignKey('ordenes_produccion.id'), nullable=True)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)


# ///////////////////////////////////////
# VENTAS 
# ///////////////////////////////////////

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    direccion_envio_id = db.Column(db.Integer, db.ForeignKey('direcciones_entrega.id'))
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('metodos_pago_cliente.id'))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    canal_venta = db.Column(db.String(50))
    estado_pedido = db.Column(db.String(50))
    total_venta = db.Column(db.Float)
    metodo_pago_fisico = db.Column(db.String(50))


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), primary_key=True)
    producto_terminado_id = db.Column(db.Integer, db.ForeignKey('productos_terminados.id'), primary_key=True)
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)


# ///////////////////////////////////////
# CAJA 
# ///////////////////////////////////////

class CorteCaja(db.Model):
    __tablename__ = 'corte_caja'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha = db.Column(db.Date)

    apertura = db.Column(db.Float)
    ventas_totales = db.Column(db.Float)
    egresos_gastos = db.Column(db.Float)
    utilidad_neta = db.Column(db.Float)

    efectivo_esperado = db.Column(db.Float)
    efectivo_real = db.Column(db.Float)
    diferencia = db.Column(db.Float)


# ///////////////////////////////////////
# TABLAS TEMPORALES 
# ///////////////////////////////////////

# E-COMMERCE

class Carrito(db.Model):
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)


class CarritoItem(db.Model):
    __tablename__ = 'carrito_items'
    id = db.Column(db.Integer, primary_key=True)
    carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'))
    producto_terminado_id = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)


# POS

class POSSesion(db.Model):
    __tablename__ = 'pos_sesion'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    abierta_en = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50))  # abierta, cerrada


class POSItem(db.Model):
    __tablename__ = 'pos_items'
    id = db.Column(db.Integer, primary_key=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('pos_sesion.id'))
    producto_terminado_id = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)


# PRODUCCION TEMPORAL

class ProduccionTemporal(db.Model):
    __tablename__ = 'produccion_temporal'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    creado_por = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)