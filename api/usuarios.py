from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appUsuarios = APIRouter()

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

class Empleado(UsuarioBase):
    id_empleado: int

class Cliente(UsuarioBase):
    id_cliente: int

# Crear empleado
@appUsuarios.post("/empleados/", response_model=Empleado)
def create_empleado(empleado: UsuarioBase):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO empleado (nombre, apellido, email, password) VALUES (%s, %s, %s, %s) RETURNING id_empleado",
            (empleado.nombre, empleado.apellido, empleado.email, empleado.password)
        )
        id_empleado = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return {**empleado.dict(), "id_empleado": id_empleado}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al crear empleado: {str(e)}")

# Crear cliente
@appUsuarios.post("/clientes/", response_model=Cliente)
def create_cliente(cliente: UsuarioBase):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO cliente (nombre, apellido, email, password) VALUES (%s, %s, %s, %s) RETURNING id_cliente",
            (cliente.nombre, cliente.apellido, cliente.email, cliente.password)
        )
        id_cliente = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return {**cliente.dict(), "id_cliente": id_cliente}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al crear cliente: {str(e)}")

# Eliminar empleado por email
@appUsuarios.delete("/empleados/{email}")
def delete_empleado(email: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM empleado WHERE email = %s", (email,))
        connection.commit()
        connection.close()
        return {"message": f"Empleado con email {email} eliminado"}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al eliminar empleado: {str(e)}")

# Eliminar cliente por email
@appUsuarios.delete("/clientes/{email}")
def delete_cliente(email: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM cliente WHERE email = %s", (email,))
        connection.commit()
        connection.close()
        return {"message": f"Cliente con email {email} eliminado"}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {str(e)}")

# Actualizar empleado por email
@appUsuarios.put("/empleados/{email}", response_model=Empleado)
def update_empleado(email: str, empleado: UsuarioBase):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE empleado SET nombre = %s, apellido = %s, password = %s WHERE email = %s RETURNING id_empleado",
            (empleado.nombre, empleado.apellido, empleado.password, email)
        )
        id_empleado = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return {**empleado.dict(), "id_empleado": id_empleado}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al actualizar empleado: {str(e)}")

# Actualizar cliente por email
@appUsuarios.put("/clientes/{email}", response_model=Cliente)
def update_cliente(email: str, cliente: UsuarioBase):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE cliente SET nombre = %s, apellido = %s, password = %s WHERE email = %s RETURNING id_cliente",
            (cliente.nombre, cliente.apellido, cliente.password, email)
        )
        id_cliente = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return {**cliente.dict(), "id_cliente": id_cliente}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al actualizar cliente: {str(e)}")

# Modificar contraseña de empleado por email
@appUsuarios.patch("/empleados/{email}/modificar-contrasena", response_model=dict)
def update_empleado_password(email: str, nueva_password: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE empleado SET password = %s WHERE email = %s", (nueva_password, email))
        connection.commit()
        connection.close()
        return {"message": f"Contraseña de empleado con email {email} modificada"}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al modificar contraseña de empleado: {str(e)}")

# Modificar contraseña de cliente por email
@appUsuarios.patch("/clientes/{email}/modificar-contrasena", response_model=dict)
def update_cliente_password(email: str, nueva_password: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE cliente SET password = %s WHERE email = %s", (nueva_password, email))
        connection.commit()
        connection.close()
        return {"message": f"Contraseña de cliente con email {email} modificada"}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=f"Error al modificar contraseña de cliente: {str(e)}")

# Obtener todos los empleados
@appUsuarios.get("/empleados/", response_model=list[Empleado])
def get_all_empleados():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM empleado")
    empleados = cursor.fetchall()
    connection.close()

    return [{"id_empleado": empleado[0], "nombre": empleado[1], "apellido": empleado[2], "email": empleado[3]} for empleado in empleados]

# Obtener todos los clientes
@appUsuarios.get("/clientes/", response_model=list[Cliente])
def get_all_clientes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    connection.close()

    return [{"id_cliente": cliente[0], "nombre": cliente[1], "apellido": cliente[2], "email": cliente[3]} for cliente in clientes]

# Obtener un empleado por email
@appUsuarios.get("/empleados/{email}", response_model=Empleado)
def get_empleado_by_email(email: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM empleado WHERE email = %s", (email,))
    empleado = cursor.fetchone()
    connection.close()

    if empleado:
        return {"id_empleado": empleado[0], "nombre": empleado[1], "apellido": empleado[2], "email": empleado[3]}
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró empleado con email {email}")

# Obtener un cliente por email
@appUsuarios.get("/clientes/{email}", response_model=Cliente)
def get_cliente_by_email(email: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cliente WHERE email = %s", (email,))
    cliente = cursor.fetchone()
    connection.close()

    if cliente:
        return {"id_cliente": cliente[0], "nombre": cliente[1], "apellido": cliente[2], "email": cliente[3]}
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró cliente con email {email}")
