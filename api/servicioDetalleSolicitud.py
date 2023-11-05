from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appServicioDetalleSolicitud = APIRouter()

# Modelo Pydantic para la tabla servicio_detalle_solicitud
class ServicioDetalleSolicitud(BaseModel):
    id_servicio: int
    id_detalle_solicitud: int
    id_solicitud: int

# Crear una nueva relación entre servicio y detalle de solicitud
@appServicioDetalleSolicitud.post("/create/", response_model=ServicioDetalleSolicitud)
def create_servicio_detalle_solicitud(servicio_detalle_solicitud: ServicioDetalleSolicitud):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO servicio_detalle_solicitud (id_servicio, id_detalle_solicitud, id_solicitud) "
        "VALUES (%s, %s, %s) RETURNING id_servicio_detalle_solicitud",
        (servicio_detalle_solicitud.id_servicio, servicio_detalle_solicitud.id_detalle_solicitud,
         servicio_detalle_solicitud.id_solicitud),
    )

    new_servicio_detalle_solicitud_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**servicio_detalle_solicitud.dict(), "id_servicio_detalle_solicitud": new_servicio_detalle_solicitud_id}

# Obtener una relación entre servicio y detalle de solicitud por su ID
@appServicioDetalleSolicitud.get("/ver/{servicio_detalle_solicitud_id}", response_model=ServicioDetalleSolicitud)
def get_servicio_detalle_solicitud(servicio_detalle_solicitud_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_servicio, id_detalle_solicitud, id_solicitud FROM servicio_detalle_solicitud WHERE id_servicio_detalle_solicitud = %s",
                   (servicio_detalle_solicitud_id,))
    servicio_detalle_solicitud = cursor.fetchone()
    connection.close()

    if servicio_detalle_solicitud is None:
        raise HTTPException(status_code=404, detail="Relación servicio-detalle-solicitud no encontrada")

    return {"id_servicio_detalle_solicitud": servicio_detalle_solicitud_id, "id_servicio": servicio_detalle_solicitud[0],
            "id_detalle_solicitud": servicio_detalle_solicitud[1], "id_solicitud": servicio_detalle_solicitud[2]}

# Actualizar una relación entre servicio y detalle de solicitud por su ID
@appServicioDetalleSolicitud.put("/update/{servicio_detalle_solicitud_id}", response_model=ServicioDetalleSolicitud)
def update_servicio_detalle_solicitud(servicio_detalle_solicitud_id: int, servicio_detalle_solicitud: ServicioDetalleSolicitud):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE servicio_detalle_solicitud SET id_servicio=%s, id_detalle_solicitud=%s, id_solicitud=%s "
        "WHERE id_servicio_detalle_solicitud = %s RETURNING id_servicio_detalle_solicitud",
        (servicio_detalle_solicitud.id_servicio, servicio_detalle_solicitud.id_detalle_solicitud,
         servicio_detalle_solicitud.id_solicitud, servicio_detalle_solicitud_id),
    )

    updated_servicio_detalle_solicitud_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_servicio_detalle_solicitud_id is None:
        raise HTTPException(status_code=404, detail="Relación servicio-detalle-solicitud no encontrada")

    return {**servicio_detalle_solicitud.dict(), "id_servicio_detalle_solicitud": updated_servicio_detalle_solicitud_id}

# Eliminar una relación entre servicio y detalle de solicitud por su ID
@appServicioDetalleSolicitud.delete("/delete/{servicio_detalle_solicitud_id}", response_model=dict)
def delete_servicio_detalle_solicitud(servicio_detalle_solicitud_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM servicio_detalle_solicitud WHERE id_servicio_detalle_solicitud = %s", (servicio_detalle_solicitud_id,))
    connection.commit()
    connection.close()

    return {"message": "Relación servicio-detalle-solicitud eliminada"}

# Obtener todas las relaciones entre servicio y detalle de solicitud
@appServicioDetalleSolicitud.get("/ver-todos/", response_model=list[ServicioDetalleSolicitud])
def get_servicios_detalle_solicitud():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_servicio_detalle_solicitud, id_servicio, id_detalle_solicitud, id_solicitud FROM servicio_detalle_solicitud")
    servicios_detalle_solicitud = cursor.fetchall()
    connection.close()

    return [{"id_servicio_detalle_solicitud": servicio[0], "id_servicio": servicio[1],
            "id_detalle_solicitud": servicio[2], "id_solicitud": servicio[3]} for servicio in servicios_detalle_solicitud]
