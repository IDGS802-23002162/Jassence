from models import db, Rol

def inicializar_roles():
    # Definimos todos los roles de Jassence en un diccionario
    roles_sistema = {
        'cliente': 'Cliente estándar del e-commerce',
        'admin': 'Administrador general del sistema Jassence',
        'ventas': 'Personal encargado de gestionar pedidos y clientes',
        'produccion': 'Personal encargado de manufactura, recetas y mermas',
        'inventario': 'Personal encargado de materias primas y proveedores'
    }

    # Iteramos sobre el diccionario para crearlos dinámicamente
    for nombre_rol, descripcion in roles_sistema.items():
        rol_existente = Rol.query.filter_by(name=nombre_rol).first()
        
        if not rol_existente:
            nuevo_rol = Rol(name=nombre_rol, description=descripcion)
            db.session.add(nuevo_rol)
            print(f"-> Rol '{nombre_rol}' creado.")
            
    # Guardamos todos los cambios de golpe al final
    db.session.commit()
    print("✅ Todos los roles han sido inicializados correctamente.")