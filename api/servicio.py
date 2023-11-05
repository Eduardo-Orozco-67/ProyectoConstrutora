from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appServicio = APIRouter()

# Modelo Pydantic para la tabla servicio
class Servicio(BaseModel):
    servicio: str
    descripcion: str

# Crear un nuevo servicio
@appServicio.post("/create/", response_model=Servicio)
def create_servicio(servicio: Servicio):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO servicio (servicio, descripcion) VALUES (%s, %s) RETURNING id_servicio",
        (servicio.servicio, servicio.descripcion),
    )

    new_servicio_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**servicio.dict(), "id_servicio": new_servicio_id}

# Obtener un servicio por su ID
@appServicio.get("/ver1/{servicio_id}", response_model=Servicio)
def get_servicio(servicio_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_servicio, servicio, descripcion FROM servicio WHERE id_servicio = %s", (servicio_id,))
    servicio = cursor.fetchone()
    connection.close()

    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    return {"id_servicio": servicio[0], "servicio": servicio[1], "descripcion": servicio[2]}

# Actualizar un servicio por su ID
@appServicio.put("/update/{servicio_id}", response_model=Servicio)
def update_servicio(servicio_id: int, servicio: Servicio):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE servicio SET servicio=%s, descripcion=%s WHERE id_servicio = %s RETURNING id_servicio",
        (servicio.servicio, servicio.descripcion, servicio_id),
    )

    updated_servicio_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_servicio_id is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    return {**servicio.dict(), "id_servicio": updated_servicio_id}

# Eliminar un servicio por su ID
@appServicio.delete("/delete/{servicio_id}", response_model=dict)
def delete_servicio(servicio_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM servicio WHERE id_servicio = %s", (servicio_id,))
    connection.commit()
    connection.close()

    return {"message": "Servicio eliminado"}

# Obtener todos los servicios
@appServicio.get("/ver-todos/", response_model=list[Servicio])
def get_servicios():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_servicio, servicio, descripcion FROM servicio")
    servicios = cursor.fetchall()
    connection.close()

    return [{"id_servicio": servicio[0], "servicio": servicio[1], "descripcion": servicio[2]} for servicio in servicios]
