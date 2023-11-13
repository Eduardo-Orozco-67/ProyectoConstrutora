from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appDetalleSolicitud = APIRouter()

# Modelo Pydantic para la tabla detalle_solicitud
class DetalleSolicitud(BaseModel):
    id_solicitud: int
    descripcion: str
    costo: float

class VerDetalleSolicitud(BaseModel):
    folio_solicitud: str
    descripcion: str
    costo: float

# Crear un nuevo detalle de solicitud
@appDetalleSolicitud.post("/create/", response_model=DetalleSolicitud)
def create_detalle_solicitud(detalle: DetalleSolicitud, folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud = id_solicitud[0]

        # Insertar el nuevo detalle de solicitud
        cursor.execute(
            "INSERT INTO detalle_solicitud (id_solicitud, descripcion, costo) "
            "VALUES (%s, %s, %s) RETURNING id_detalle_solicitud",
            (id_solicitud, detalle.descripcion, detalle.costo),
        )

        new_detalle_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el detalle de solicitud: {str(e)}")

    finally:
        connection.close()

    return {**detalle.dict(), "id_detalle_solicitud": new_detalle_id}

@appDetalleSolicitud.get("/ver1/{folio_solicitud}", response_model=VerDetalleSolicitud)
def get_detalle_solicitud(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT ds.descripcion, ds.costo "
        "FROM detalle_solicitud ds "
        "INNER JOIN solicitud_proyecto sp ON ds.id_solicitud = sp.id_solicitud "
        "WHERE sp.folio_solicitud = %s",
        (folio_solicitud,),
    )

    detalle = cursor.fetchone()
    connection.close()

    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle de solicitud no encontrado")

    return {"folio_solicitud": folio_solicitud, "descripcion": detalle[0], "costo": detalle[1]}

# Actualizar un detalle de solicitud por su ID
@appDetalleSolicitud.put("/update/{folio_solicitud}", response_model=DetalleSolicitud)
def update_detalle_solicitud(update: DetalleSolicitud, folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud = id_solicitud[0]

        # Actualizar el detalle de solicitud
        cursor.execute(
            "UPDATE detalle_solicitud SET descripcion=%s, costo=%s "
            "WHERE id_solicitud = %s RETURNING id_detalle_solicitud",
            (update.descripcion, update.costo, id_solicitud),
        )

        updated_detalle_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el detalle de solicitud: {str(e)}")

    finally:
        connection.close()

    return {**update.dict(), "id_detalle_solicitud": updated_detalle_id}

# Eliminar un detalle de solicitud por su ID
@appDetalleSolicitud.delete("/delete/{folio_solicitud}", response_model=dict)
def delete_detalle_solicitud(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        # Eliminar el detalle de solicitud
        cursor.execute("DELETE FROM detalle_solicitud WHERE id_solicitud = %s", (id_solicitud[0],))
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el detalle de solicitud: {str(e)}")

    finally:
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
