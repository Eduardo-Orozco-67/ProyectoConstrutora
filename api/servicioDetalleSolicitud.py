from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appServicioDetalleSolicitud = APIRouter()

# Modelo Pydantic para la tabla servicio_detalle_solicitud
class ServicioDetalleSolicitud(BaseModel):
    id_servicio: int
    id_detalle_solicitud: int
    id_solicitud: int

class ServicioResponse(BaseModel):
    id_servicio: int
    servicio: str

# Crear una nueva relación entre servicio y detalle de solicitud
@appServicioDetalleSolicitud.post("/create/", response_model=ServicioDetalleSolicitud)
def create_servicio_detalle_solicitud(
    id_servicio: int,
    folio_solicitud: str
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute(
            "SELECT sp.id_solicitud, ds.id_detalle_solicitud "
            "FROM detalle_solicitud ds "
            "INNER JOIN solicitud_proyecto sp ON ds.id_solicitud = sp.id_solicitud "
            "WHERE sp.folio_solicitud = %s",
            (folio_solicitud,)
        )
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud, id_detalle_solicitud = result

        # Insertar el nuevo servicio_detalle_solicitud
        cursor.execute(
            "INSERT INTO servicio_detalle_solicitud (id_servicio, id_detalle_solicitud, id_solicitud) "
            "VALUES (%s, %s, %s) RETURNING id_servicio_detalle_solicitud",
            (id_servicio, id_detalle_solicitud, id_solicitud),
        )

        new_servicio_detalle_solicitud_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el servicio_detalle_solicitud: {str(e)}")

    finally:
        connection.close()

    return {
        "id_servicio_detalle_solicitud": new_servicio_detalle_solicitud_id,
        "id_servicio": id_servicio,
        "id_detalle_solicitud": id_detalle_solicitud,
        "id_solicitud": id_solicitud,
    }


# Obtener una relación entre servicio y detalle de solicitud por folio
@appServicioDetalleSolicitud.get("/ver-servicios-folio/{folio_solicitud}", response_model=list[ServicioResponse])
def get_servicios_by_detalle_solicitud(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute(
            "SELECT sp.id_solicitud, sds.id_servicio, sds.id_detalle_solicitud "
            "FROM servicio_detalle_solicitud sds "
            "INNER JOIN detalle_solicitud ds ON sds.id_detalle_solicitud = ds.id_detalle_solicitud "
            "INNER JOIN solicitud_proyecto sp ON ds.id_solicitud = sp.id_solicitud "
            "WHERE sp.folio_solicitud = %s",
            (folio_solicitud,)
        )
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud, _, id_detalle_solicitud = result  # Corregir aquí

        # Obtener todos los servicios que comparten el mismo id de detalle y solicitud
        cursor.execute(
            "SELECT s.id_servicio, s.servicio "
            "FROM servicio_detalle_solicitud sds "
            "INNER JOIN servicio s ON sds.id_servicio = s.id_servicio "
            "WHERE sds.id_detalle_solicitud = %s AND sds.id_solicitud = %s",
            (id_detalle_solicitud, id_solicitud)
        )
        servicios = cursor.fetchall()

    finally:
        connection.close()

    servicios_list = [ServicioResponse(id_servicio=servicio[0], servicio=servicio[1]) for servicio in servicios]
    return servicios_list

# eliminar un servicio en especifico de un folio en especifico
@appServicioDetalleSolicitud.delete("/delete/{folio_solicitud}/{id_servicio}", response_model=dict)
def delete_servicio_detalle_solicitud(folio_solicitud: str, id_servicio: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute(
            "SELECT sp.id_solicitud, sds.id_servicio_detalle_solicitud "
            "FROM servicio_detalle_solicitud sds "
            "INNER JOIN detalle_solicitud ds ON sds.id_detalle_solicitud = ds.id_detalle_solicitud "
            "INNER JOIN solicitud_proyecto sp ON ds.id_solicitud = sp.id_solicitud "
            "WHERE sp.folio_solicitud = %s AND sds.id_servicio = %s",
            (folio_solicitud, id_servicio)
        )
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Relación servicio-detalle-solicitud no encontrada")

        _, id_servicio_detalle_solicitud = result

        # Eliminar la relación servicio-detalle-solicitud
        cursor.execute("DELETE FROM servicio_detalle_solicitud WHERE id_servicio_detalle_solicitud = %s",
                       (id_servicio_detalle_solicitud,))
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la relación servicio-detalle-solicitud: {str(e)}")

    finally:
        connection.close()

    return {"message": "Relación servicio-detalle-solicitud eliminada"}
