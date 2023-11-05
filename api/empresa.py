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


# Crear una nueva empresa
@appEmpresa.post("/create/", response_model=Empresa)
def create_empresa(empresa: Empresa):
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


# Obtener una empresa por su ID
@appEmpresa.get("/ver1/{empresa_id}", response_model=Empresa)
def get_empresa(empresa_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_empresa, nombre, direccion, telefono, correo FROM empresa WHERE id_empresa = %s",
                   (empresa_id,))
    empresa = cursor.fetchone()
    connection.close()

    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return {"id_empresa": empresa[0], "nombre": empresa[1], "direccion": empresa[2], "telefono": empresa[3],
            "correo": empresa[4]}


# Actualizar una empresa por su ID
@appEmpresa.put("/update/{empresa_id}", response_model=Empresa)
def update_empresa(empresa_id: int, empresa: Empresa):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE empresa SET nombre=%s, direccion=%s, telefono=%s, correo=%s WHERE id_empresa = %s RETURNING id_empresa",
        (empresa.nombre, empresa.direccion, empresa.telefono, empresa.correo, empresa_id),
    )

    updated_empresa_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_empresa_id is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return {**empresa.dict(), "id_empresa": updated_empresa_id}


# Eliminar una empresa por su ID
@appEmpresa.delete("/delete/{empresa_id}", response_model=dict)
def delete_empresa(empresa_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM empresa WHERE id_empresa = %s", (empresa_id,))
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