from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appServicio = APIRouter()

# Modelo Pydantic para la tabla servicio
class Servicio(BaseModel):
    servicio: str
    descripcion: str


# Crear un servicio
@appServicio.post("/create/", response_model=Servicio)
def create_servicio(servicio: Servicio):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si ya existe un servicio con el mismo nombre
        cursor.execute("SELECT id_servicio FROM servicio WHERE servicio = %s", (servicio.servicio,))
        existing_servicio = cursor.fetchone()

        if existing_servicio:
            raise HTTPException(status_code=400, detail="Ya existe un servicio con ese nombre")

        # Insertar el nuevo servicio
        cursor.execute(
            "INSERT INTO servicio (servicio, descripcion) VALUES (%s, %s) RETURNING id_servicio",
            (servicio.servicio, servicio.descripcion),
        )

        new_servicio_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el servicio: {str(e)}")

    finally:
        connection.close()

    return {**servicio.dict(), "id_servicio": new_servicio_id}

# Obtener un servicio por su nombre
@appServicio.get("/ver1/{nombre_servicio}", response_model=Servicio)
def get_servicio(nombre_servicio: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_servicio, servicio, descripcion FROM servicio WHERE servicio = %s", (nombre_servicio,))
    servicio = cursor.fetchone()
    connection.close()

    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    return {"id_servicio": servicio[0], "servicio": servicio[1], "descripcion": servicio[2]}


# Actualizar un servicio por su nombre (solo la descripción)
# Actualizar la descripción de un servicio por su nombre
@appServicio.patch("/update/{nombre_servicio}", response_model=Servicio)
def update_servicio(nombre_servicio: str, nueva_descripcion: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si el servicio existe
        cursor.execute("SELECT id_servicio FROM servicio WHERE servicio = %s", (nombre_servicio,))
        existing_servicio = cursor.fetchone()

        if existing_servicio is None:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # Actualizar la descripción del servicio
        cursor.execute(
            "UPDATE servicio SET descripcion=%s WHERE servicio = %s RETURNING id_servicio",
            (nueva_descripcion, nombre_servicio),
        )

        updated_servicio_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la descripción del servicio: {str(e)}")

    finally:
        connection.close()

    return {"id_servicio": updated_servicio_id, "servicio": nombre_servicio, "descripcion": nueva_descripcion}

# Eliminar un servicio por su nombre
@appServicio.delete("/delete/{nombre_servicio}", response_model=dict)
def delete_servicio(nombre_servicio: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM servicio WHERE servicio = %s", (nombre_servicio,))
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
