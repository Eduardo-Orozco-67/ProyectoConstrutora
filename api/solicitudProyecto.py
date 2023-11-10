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

class SolicitudProyectover(BaseModel):
    id_solicitud: int
    nombre_empresa: str
    fecha: str
    monto_presupuesto: float
    monto_anticipo: float
    folio_solicitud: str
    estado: str

# Crear una nueva solicitud de proyecto
from fastapi import HTTPException

@appSolicitudProyecto.post("/create/", response_model=SolicitudProyecto)
def create_solicitud_proyecto(
    nombre_empresa: str,
    fecha: str,
    monto_presupuesto: float,
    monto_anticipo: float,
    folio_solicitud: str,
    estado: str
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si el folio ya existe en la base de datos
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        existing_solicitud = cursor.fetchone()

        if existing_solicitud:
            raise HTTPException(status_code=400, detail="Ya existe una solicitud con este folio")

        # Obtener el ID de la empresa por su nombre
        cursor.execute("SELECT id_empresa FROM empresa WHERE nombre = %s", (nombre_empresa,))
        empresa_id = cursor.fetchone()

        if not empresa_id:
            raise HTTPException(status_code=404, detail="No se encontró la empresa con el nombre proporcionado")

        # Convertir empresa_id a int
        empresa_id = empresa_id[0]

        # Insertar la nueva solicitud
        cursor.execute(
            "INSERT INTO solicitud_proyecto (id_empresa, fecha, monto_presupuesto, monto_anticipo, folio_solicitud, estado) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_solicitud",
            (empresa_id, fecha, monto_presupuesto, monto_anticipo, folio_solicitud, estado),
        )

        new_solicitud_id = cursor.fetchone()[0]
        connection.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la solicitud: {str(e)}")
    finally:
        connection.close()

    return {
        "id_empresa": empresa_id,
        "fecha": fecha,
        "monto_presupuesto": monto_presupuesto,
        "monto_anticipo": monto_anticipo,
        "folio_solicitud": folio_solicitud,
        "estado": estado,
        "id_solicitud": new_solicitud_id
    }


# Obtener una solicitud de proyecto por su folio_solicitud
@appSolicitudProyecto.get("/ver1/{folio_solicitud}", response_model=SolicitudProyectover)
def get_solicitud_proyecto_by_folio(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT s.id_solicitud, e.nombre as nombre_empresa, s.fecha, s.monto_presupuesto, s.monto_anticipo, s.folio_solicitud, s.estado "
        "FROM solicitud_proyecto s "
        "INNER JOIN empresa e ON s.id_empresa = e.id_empresa")
    solicitud = cursor.fetchone()
    connection.close()

    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

    return {
        "id_solicitud": solicitud[0],
        "nombre_empresa": solicitud[1],
        "fecha": str(solicitud[2]),  # Convertir la fecha a cadena
        "monto_presupuesto": solicitud[3],
        "monto_anticipo": solicitud[4],
        "folio_solicitud": solicitud[5],
        "estado": solicitud[6],
    }

# Actualizar una solicitud de proyecto por su folio_solicitud
@appSolicitudProyecto.put("/update/{folio_solicitud}", response_model=SolicitudProyecto)
def update_solicitud_proyecto_by_folio(folio_solicitud: str, solicitud: SolicitudProyecto):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE solicitud_proyecto SET id_empresa=%s, fecha=%s, monto_presupuesto=%s, monto_anticipo=%s, "
        "folio_solicitud=%s, estado=%s WHERE folio_solicitud = %s RETURNING id_solicitud",
        (
            solicitud.id_empresa,
            solicitud.fecha,
            solicitud.monto_presupuesto,
            solicitud.monto_anticipo,
            solicitud.folio_solicitud,
            solicitud.estado,
            folio_solicitud,
        ),
    )

    updated_solicitud_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_solicitud_id is None:
        raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

    return {**solicitud.dict(), "id_solicitud": updated_solicitud_id}

# Eliminar una solicitud de proyecto por su folio_solicitud
@appSolicitudProyecto.delete("/delete/{folio_solicitud}", response_model=dict)
def delete_solicitud_proyecto_by_folio(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
    connection.commit()
    connection.close()

    return {"message": "Solicitud de proyecto eliminada"}

@appSolicitudProyecto.patch("/actualizar-estado/{folio_solicitud}")
def update_estado_solicitud(folio_solicitud: str, estado: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si la solicitud de proyecto existe
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        # Actualizar el estado de la solicitud por folio
        cursor.execute(
            "UPDATE solicitud_proyecto SET estado = %s WHERE folio_solicitud = %s RETURNING id_solicitud",
            (estado, folio_solicitud),
        )

        updated_solicitud_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado de la solicitud: {str(e)}")

    finally:
        connection.close()

    return {"folio_solicitud": folio_solicitud, "estado_actualizado": estado, "id_solicitud": updated_solicitud_id}

# Obtener todas las solicitudes de proyecto
@appSolicitudProyecto.get("/ver-todas", response_model=list[SolicitudProyectover])
def get_solicitudes_proyecto():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT s.id_solicitud, e.nombre as nombre_empresa, s.fecha, s.monto_presupuesto, s.monto_anticipo, s.folio_solicitud, s.estado "
                   "FROM solicitud_proyecto s "
                   "INNER JOIN empresa e ON s.id_empresa = e.id_empresa")
    solicitudes_proyecto = cursor.fetchall()
    connection.close()

    return [
        {
            "id_solicitud": solicitud[0],
            "nombre_empresa": solicitud[1],
            "fecha": str(solicitud[2]),  # Convertir la fecha a cadena
            "monto_presupuesto": solicitud[3],
            "monto_anticipo": solicitud[4],
            "folio_solicitud": solicitud[5],
            "estado": solicitud[6],
        }
        for solicitud in solicitudes_proyecto
    ]
