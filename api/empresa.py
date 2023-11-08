from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appEmpresa = APIRouter()

# Modelo Pydantic para la tabla empresa
class Empresa(BaseModel):
    nombre: str
    direccion: str
    telefono: int
    correo: str


# Verificar si ya existe una empresa con el mismo nombre
def empresa_existe(nombre_empresa):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id_empresa FROM empresa WHERE nombre = %s", (nombre_empresa,))
    empresa = cursor.fetchone()
    connection.close()
    return empresa is not None


# Obtener una empresa por su ID o nombre
@appEmpresa.get("/ver1/{empresa_id_or_nombre}", response_model=Empresa)
def get_empresa(empresa_id_or_nombre: str):
    connection = get_connection()
    cursor = connection.cursor()

    if empresa_id_or_nombre.isdigit():
        # Si el parámetro es un número, asumimos que es un ID
        cursor.execute("SELECT id_empresa, nombre, direccion, telefono, correo FROM empresa WHERE id_empresa = %s", (int(empresa_id_or_nombre),))
    else:
        # Si el parámetro no es un número, asumimos que es el nombre de la empresa
        cursor.execute("SELECT id_empresa, nombre, direccion, telefono, correo FROM empresa WHERE nombre = %s", (empresa_id_or_nombre,))

    empresa = cursor.fetchone()
    connection.close()

    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return {"id_empresa": empresa[0], "nombre": empresa[1], "direccion": empresa[2], "telefono": empresa[3], "correo": empresa[4]}


# Crear una nueva empresa
@appEmpresa.post("/create/", response_model=Empresa)
def create_empresa(empresa: Empresa):
    if empresa_existe(empresa.nombre):
        raise HTTPException(status_code=400, detail="La empresa con el mismo nombre ya existe")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO empresa (nombre, direccion, telefono, correo) VALUES (%s, %s, %s, %s) RETURNING id_empresa",
        (empresa.nombre, empresa.direccion, empresa.telefono, empresa.correo),
    )

    new_empresa_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**empresa.dict(), "id_empresa": new_empresa_id}


# Actualizar una empresa por su nombre
@appEmpresa.put("/update/{nombre_empresa}", response_model=Empresa)
def update_empresa(nombre_empresa: str, empresa: Empresa):
    if not empresa_existe(nombre_empresa):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE empresa SET nombre=%s, direccion=%s, telefono=%s, correo=%s WHERE nombre = %s RETURNING id_empresa",
        (empresa.nombre, empresa.direccion, empresa.telefono, empresa.correo, nombre_empresa),
    )

    updated_empresa_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**empresa.dict(), "id_empresa": updated_empresa_id}


# Eliminar una empresa por su nombre
@appEmpresa.delete("/delete/{nombre_empresa}", response_model=dict)
def delete_empresa(nombre_empresa: str):
    if not empresa_existe(nombre_empresa):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM empresa WHERE nombre = %s", (nombre_empresa,))
    connection.commit()
    connection.close()

    return {"message": "Empresa eliminada"}


# Obtener todas las empresas
@appEmpresa.get("/ver-todas", response_model=list[Empresa])
def get_empresas():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_empresa, nombre, direccion, telefono, correo FROM empresa")
    empresas = cursor.fetchall()
    connection.close()

    return [{"id_empresa": empresa[0], "nombre": empresa[1], "direccion": empresa[2], "telefono": empresa[3],
             "correo": empresa[4]} for empresa in empresas]