from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appProyectoSupervisor = APIRouter()

# Modelo Pydantic para la tabla proyecto_supervisor
class ProyectoSupervisor(BaseModel):
    id_proyecto: int
    id_supervisor: int

class ProyectoSupervisorResponse(BaseModel):
    nombre_supervisor: str
    folio_proyecto: str

# Crear una nueva relación entre proyecto y supervisor
@appProyectoSupervisor.post("/create/", response_model=ProyectoSupervisor)
def create_proyecto_supervisor(folio_solicitud: str, telefono_supervisor: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_proyecto correspondiente al folio_solicitud
        cursor.execute("SELECT id_proyecto FROM proyecto WHERE id_solicitud = (SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s)",
                       (folio_solicitud,))
        id_proyecto = cursor.fetchone()

        if id_proyecto is None:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado para el folio de solicitud proporcionado")

        # Verificar si el supervisor ya tiene asignado el proyecto
        cursor.execute(
            "SELECT id_proyecto_supervisor FROM proyecto_supervisor "
            "WHERE id_proyecto = %s AND id_supervisor = (SELECT id_supervisor FROM supervisor WHERE telefono = %s)",
            (id_proyecto[0], telefono_supervisor)
        )
        existing_relation = cursor.fetchone()

        if existing_relation:
            raise HTTPException(status_code=400, detail="El supervisor ya tiene asignado este proyecto")

        # Buscar el ID del supervisor por su número de teléfono
        cursor.execute("SELECT id_supervisor FROM supervisor WHERE telefono = %s", (telefono_supervisor,))
        id_supervisor = cursor.fetchone()

        if id_supervisor is None:
            raise HTTPException(status_code=404, detail="Supervisor no encontrado")

        # Insertar la relación proyecto-supervisor
        cursor.execute(
            "INSERT INTO proyecto_supervisor (id_proyecto, id_supervisor) VALUES (%s, %s) RETURNING id_proyecto_supervisor",
            (id_proyecto[0], id_supervisor[0]),
        )

        new_proyecto_supervisor_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la relación proyecto-supervisor: {str(e)}")

    finally:
        connection.close()

    return {"id_proyecto_supervisor": new_proyecto_supervisor_id, "id_proyecto": id_proyecto[0], "id_supervisor": id_supervisor[0]}

# Obtener los proyectos de un supervisor por telefono del super
@appProyectoSupervisor.get("/ver/{telefono_supervisor}", response_model=list[ProyectoSupervisorResponse])
def get_proyectos_by_supervisor(telefono_supervisor: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Buscar el ID del supervisor por su número de teléfono
        cursor.execute("SELECT id_supervisor, nombre FROM supervisor WHERE telefono = %s", (telefono_supervisor,))
        supervisor_info = cursor.fetchone()

        if supervisor_info is None:
            raise HTTPException(status_code=404, detail="Supervisor no encontrado")

        id_supervisor, nombre_supervisor = supervisor_info

        # Obtener todos los proyectos en los que está trabajando el supervisor
        cursor.execute(
            "SELECT sp.folio_solicitud, s.nombre as nombre_supervisor "
            "FROM proyecto p "
            "INNER JOIN proyecto_supervisor ps ON p.id_proyecto = ps.id_proyecto "
            "INNER JOIN supervisor s ON ps.id_supervisor = s.id_supervisor "
            "INNER JOIN solicitud_proyecto sp ON p.id_solicitud = sp.id_solicitud "
            "WHERE s.id_supervisor = %s",
            (id_supervisor,)
        )
        proyectos_supervisor = cursor.fetchall()
        connection.close()

        # Crear la lista de resultados
        result_list = [
            ProyectoSupervisorResponse(
                nombre_supervisor=nombre_supervisor,
                folio_proyecto=proyecto[0],
            )
            for proyecto in proyectos_supervisor
        ]

        return result_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos de supervisor: {str(e)}")

    finally:
        connection.close()

# Eliminar una relación entre proyecto y supervisor por su ID
@appProyectoSupervisor.delete("/delete/{telefono_supervisor}/{id_proyecto}", response_model=dict)
def delete_proyecto_supervisor(telefono_supervisor: int, id_proyecto: str):
    connection = get_connection()
    cursor = connection.cursor()

    # Buscar el ID del supervisor por su número de teléfono
    cursor.execute("SELECT id_supervisor FROM supervisor WHERE telefono = %s", (telefono_supervisor,))
    id_supervisor = cursor.fetchone()

    if id_supervisor is None:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado")

    # Eliminar la relación proyecto-supervisor por teléfono del supervisor y folio del proyecto
    cursor.execute(
        "DELETE FROM proyecto_supervisor WHERE id_supervisor = %s AND id_proyecto = %s",
        (id_supervisor[0], id_proyecto)
    )
    connection.commit()
    connection.close()

    return {"message": "Relación proyecto-supervisor eliminada"}

# Obtener todas las relaciones entre proyecto y supervisor
# Método para obtener todos los proyectos de supervisores con folios
@appProyectoSupervisor.get("/ver-todos/", response_model=list[ProyectoSupervisorResponse])
def get_proyectos_supervisor():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener todos los proyectos de supervisores con sus folios
        cursor.execute(
            "SELECT sp.folio_solicitud, s.nombre as nombre_supervisor "
            "FROM proyecto p "
            "INNER JOIN proyecto_supervisor ps ON p.id_proyecto = ps.id_proyecto "
            "INNER JOIN supervisor s ON ps.id_supervisor = s.id_supervisor "
            "INNER JOIN solicitud_proyecto sp ON p.id_solicitud = sp.id_solicitud "
            "WHERE s.id_supervisor = 1"
        )
        proyectos_supervisor = cursor.fetchall()
        connection.close()

        # Crear la lista de resultados
        result_list = [{"nombre_supervisor": proyecto[1], "folio_proyecto": proyecto[0]} for proyecto in proyectos_supervisor]
        return result_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener todos los proyectos de supervisores: {str(e)}")

    finally:
        connection.close()