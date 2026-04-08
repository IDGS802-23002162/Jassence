from datetime import datetime
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
    cliente = db.relationship(
        "Cliente",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

class LogAuditoria(db.Model):
    __tablename__ = 'log_auditoria'
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
    id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True
    )
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship(
        "Usuario",
        back_populates="cliente"
    )

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
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    # Identificadores de Stripe (Seguros)
    stripe_customer_id = db.Column(db.String(50), nullable=False)
    stripe_payment_method_id = db.Column(db.String(50), nullable=False)
    
    # Datos para mostrar en la interfaz (Seguros)
    tipo_tarjeta = db.Column(db.String(20)) # Ej: "Visa"
    ultimos_4 = db.Column(db.String(4))    # Ej: "4242"
    exp_mes = db.Column(db.Integer)
    exp_anio = db.Column(db.Integer)
    estado = db.Column(db.Boolean, default=True)
    es_principal = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)


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
    tipo = db.Column(db.String(50)) 


class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    tipo_insumos = db.Column(db.String(100))

    activo = db.Column(db.Boolean, default=True)
    compras = db.relationship('Compra', backref='proveedor', lazy=True)


class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    archivo_factura = db.Column(db.String(255))

    estado = db.Column(db.String(50), default="pendiente")  # pendiente, pedido, entregado, cancelado

    notas = db.Column(db.Text) 
    total = db.Column(db.Float, default=0.0)
    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True, cascade="all, delete-orphan")
    usuario = db.relationship('Usuario', backref='compras_registradas', lazy=True)

class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compras'
    
    # 1. Agregamos un ID propio como Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'))
    
    # 2. Hacemos que la materia prima sea opcional (nullable=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=True)
    
    # 3. Agregamos la relación con la Presentación (nullable=True)
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentaciones.id'), nullable=True)
    
    # 4. Campo de control para saber si es líquido o envase
    tipo_item = db.Column(db.String(20), default='materia') # 'materia' o 'presentacion'

    # Los demás campos quedan igual
    cantidad_comprada = db.Column(db.Float)
    unidad_compra = db.Column(db.String(50))
    precio_unitario = db.Column(db.Float)
    multiplicador = db.Column(db.Float, default=1.0)
    subtotal = db.Column(db.Float)
    
    materia_prima = db.relationship('MateriaPrima', backref='detalles_compra', lazy=True)
    presentacion = db.relationship('Presentacion', backref='detalles_compra', lazy=True)
    
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

    productos_terminados = db.relationship('ProductoTerminado', backref='receta', lazy=True)

    detalles = db.relationship('DetalleReceta', backref='receta', lazy=True, cascade="all, delete-orphan")


class DetalleReceta(db.Model):
    __tablename__ = 'detalle_recetas'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    porcentaje = db.Column(db.Float)
    tipo_componente = db.Column(db.String(50))

    materia_prima = db.relationship('MateriaPrima', backref='detalles_receta')


class Presentacion(db.Model):
    __tablename__ = 'presentaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    mililitros = db.Column(db.Integer)
    stock_botes = db.Column(db.Integer, default=0)
    productos_terminados = db.relationship('ProductoTerminado', back_populates='presentacion', lazy=True)


class ProductoTerminado(db.Model):
    __tablename__= 'productos_terminados'
    __table_args__= (db.UniqueConstraint('receta_id', 'presentacion_id', name='unique_producto'),)
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentaciones.id'))
    stock_disponible_venta = db.Column(db.Integer)
    stock_minimo = db.Column(db.Integer)
    precio_venta = db.Column(db.Float)
    estado = db.Column(db.String(50))
    stock_comprometido = db.Column(db.Integer)
    
    presentacion = db.relationship('Presentacion', back_populates='productos_terminados')


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

    estado = db.Column(db.String(50))

    receta = db.relationship('Receta')
    producto_terminado = db.relationship('ProductoTerminado')
    responsable = db.relationship('Usuario')


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
    pasarela_online = db.Column(db.String(30))
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('metodos_pago_cliente.id'))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    canal_venta = db.Column(db.String(50))
    estado_pedido = db.Column(db.String(50))
    total_venta = db.Column(db.Float)
    metodo_pago_fisico = db.Column(db.String(50))

    sesion_id = db.Column(db.Integer, db.ForeignKey('pos_sesion.id'), nullable=True)
    usuario = db.relationship('Usuario', backref='ventas_realizadas')
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade="all, delete-orphan")


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), primary_key=True)
    producto_terminado_id = db.Column(db.Integer, db.ForeignKey('productos_terminados.id'), primary_key=True)
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)

    producto_terminado = db.relationship('ProductoTerminado', backref='detalles_venta', lazy=True)


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
    sesion_id = db.Column(db.Integer, db.ForeignKey('pos_sesion.id'), nullable=True)

    sesion_id = db.Column(db.Integer, db.ForeignKey('pos_sesion.id'), nullable=True)


class EgresoCaja(db.Model):
    __tablename__ = 'egresos_caja'
    id = db.Column(db.Integer, primary_key=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('pos_sesion.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    monto = db.Column(db.Float, nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# ///////////////////////////////////////
# TABLAS TEMPORALES 
# ///////////////////////////////////////

# E-COMMERCE

class Carrito(db.Model):
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('CarritoItem', backref='carrito', lazy=True)


class CarritoItem(db.Model):
    __tablename__ = 'carrito_items'
    id = db.Column(db.Integer, primary_key=True)
    carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'))
    cantidad = db.Column(db.Integer)
    producto_terminado_id = db.Column(db.Integer, db.ForeignKey('productos_terminados.id'))
    producto_terminado = db.relationship('ProductoTerminado')


# POS

class POSSesion(db.Model):
    __tablename__ = 'pos_sesion'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    abierta_en = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50))
    monto_apertura = db.Column(db.Float, default=0.0)
    cerrada_en = db.Column(db.DateTime, nullable=True)
    
    ventas = db.relationship('Venta', backref='sesion_caja', lazy=True)
    egresos = db.relationship('EgresoCaja', backref='sesion_caja', lazy=True)
    cortes = db.relationship('CorteCaja', backref='sesion_caja', lazy=True)  # abierta, cerrada

    monto_apertura = db.Column(db.Float, default=0.0)
    cerrada_en = db.Column(db.DateTime, nullable=True)


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

    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentaciones.id'))
    estatus = db.Column(db.String(20), default='pendiente')
    presentacion = db.relationship('Presentacion')


