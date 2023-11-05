from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appSolicitudProyecto = APIRouter()

# Modelo Pydantic para la tabla solicitud_proyecto
class SolicitudProyecto(BaseModel):
    id_empresa: int
    fecha: str
    monto_presupuesto: float
    monto_anticipo: float
    folio_solicitud: str
    estado: str

# Crear una nueva solicitud de proyecto
@appSolicitudProyecto.post("/create/", response_model=SolicitudProyecto)
def create_solicitud_proyecto(solicitud: SolicitudProyecto):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO solicitud_proyecto (id_empresa, fecha, monto_presupuesto, monto_anticipo, folio_solicitud, estado) "
        "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_solicitud",
        (solicitud.id_empresa, solicitud.fecha, solicitud.monto_presupuesto, solicitud.monto_anticipo,
         solicitud.folio_solicitud, solicitud.estado),
    )

    new_solicitud_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**solicitud.dict(), "id_solicitud": new_solicitud_id}

# Obtener una solicitud de proyecto por su ID
@appSolicitudProyecto.get("/ver1/{solicitud_id}", response_model=SolicitudProyecto)
def get_solicitud_proyecto(solicitud_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_solicitud, id_empresa, fecha, monto_presupuesto, monto_anticipo, folio_solicitud, estado "
                   "FROM solicitud_proyecto WHERE id_solicitud = %s", (solicitud_id,))
    solicitud = cursor.fetchone()
    connection.close()

    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

    return {"id_solicitud": solicitud[0], "id_empresa": solicitud[1], "fecha": solicitud[2],
            "monto_presupuesto": solicitud[3], "monto_anticipo": solicitud[4], "folio_solicitud": solicitud[5],
            "estado": solicitud[6]}

# Actualizar una solicitud de proyecto por su ID
@appSolicitudProyecto.put("/update/{solicitud_id}", response_model=SolicitudProyecto)
def update_solicitud_proyecto(solicitud_id: int, solicitud: SolicitudProyecto):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE solicitud_proyecto SET id_empresa=%s, fecha=%s, monto_presupuesto=%s, monto_anticipo=%s, "
        "folio_solicitud=%s, estado=%s WHERE id_solicitud = %s RETURNING id_solicitud",
        (solicitud.id_empresa, solicitud.fecha, solicitud.monto_presupuesto, solicitud.monto_anticipo,
         solicitud.folio_solicitud, solicitud.estado, solicitud_id),
    )

    updated_solicitud_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_solicitud_id is None:
        raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

    return {**solicitud.dict(), "id_solicitud": updated_solicitud_id}

# Eliminar una solicitud de proyecto por su ID
@appSolicitudProyecto.delete("/delete/{solicitud_id}", response_model=dict)
def delete_solicitud_proyecto(solicitud_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM solicitud_proyecto WHERE id_solicitud = %s", (solicitud_id,))
    connection.commit()
    connection.close()

    return {"message": "Solicitud de proyecto eliminada"}

# Obtener todas las solicitudes de proyecto
@appSolicitudProyecto.get("/ver-todas", response_model=list[SolicitudProyecto])
def get_solicitudes_proyecto():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_solicitud, id_empresa, fecha, monto_presupuesto, monto_anticipo, folio_solicitud, estado "
                   "FROM solicitud_proyecto")
    solicitudes_proyecto = cursor.fetchall()
    connection.close()

    return [{"id_solicitud": solicitud[0], "id_empresa": solicitud[1], "fecha": solicitud[2],
            "monto_presupuesto": solicitud[3], "monto_anticipo": solicitud[4], "folio_solicitud": solicitud[5],
            "estado": solicitud[6]} for solicitud in solicitudes_proyecto]
