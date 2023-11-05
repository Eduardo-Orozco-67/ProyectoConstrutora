from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appDetalleSolicitud = APIRouter()

# Modelo Pydantic para la tabla detalle_solicitud
class DetalleSolicitud(BaseModel):
    id_solicitud: int
    descripcion: str
    costo: float

# Crear un nuevo detalle de solicitud
@appDetalleSolicitud.post("/create/", response_model=DetalleSolicitud)
def create_detalle_solicitud(detalle: DetalleSolicitud):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO detalle_solicitud (id_solicitud, descripcion, costo) VALUES (%s, %s, %s) RETURNING id_detalle_solicitud",
        (detalle.id_solicitud, detalle.descripcion, detalle.costo),
    )

    new_detalle_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**detalle.dict(), "id_detalle_solicitud": new_detalle_id}

# Obtener un detalle de solicitud por su ID
@appDetalleSolicitud.get("/ver1/{detalle_id}", response_model=DetalleSolicitud)
def get_detalle_solicitud(detalle_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_solicitud, descripcion, costo FROM detalle_solicitud WHERE id_detalle_solicitud = %s", (detalle_id,))
    detalle = cursor.fetchone()
    connection.close()

    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle de solicitud no encontrado")

    return {"id_detalle_solicitud": detalle_id, "id_solicitud": detalle[0], "descripcion": detalle[1], "costo": detalle[2]}

# Actualizar un detalle de solicitud por su ID
@appDetalleSolicitud.put("/update/{detalle_id}", response_model=DetalleSolicitud)
def update_detalle_solicitud(detalle_id: int, detalle: DetalleSolicitud):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE detalle_solicitud SET id_solicitud=%s, descripcion=%s, costo=%s WHERE id_detalle_solicitud = %s RETURNING id_detalle_solicitud",
        (detalle.id_solicitud, detalle.descripcion, detalle.costo, detalle_id),
    )

    updated_detalle_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_detalle_id is None:
        raise HTTPException(status_code=404, detail="Detalle de solicitud no encontrado")

    return {**detalle.dict(), "id_detalle_solicitud": updated_detalle_id}

# Eliminar un detalle de solicitud por su ID
@appDetalleSolicitud.delete("/delete/{detalle_id}", response_model=dict)
def delete_detalle_solicitud(detalle_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM detalle_solicitud WHERE id_detalle_solicitud = %s", (detalle_id,))
    connection.commit()
    connection.close()

    return {"message": "Detalle de solicitud eliminado"}

# Obtener todos los detalles de solicitud
@appDetalleSolicitud.get("/ver-todos/", response_model=list[DetalleSolicitud])
def get_detalles_solicitud():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_detalle_solicitud, id_solicitud, descripcion, costo FROM detalle_solicitud")
    detalles_solicitud = cursor.fetchall()
    connection.close()

    return [{"id_detalle_solicitud": detalle[0], "id_solicitud": detalle[1], "descripcion": detalle[2], "costo": detalle[3]} for detalle in detalles_solicitud]
