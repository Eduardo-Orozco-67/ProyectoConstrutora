from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appProyectoSupervisor = APIRouter()

# Modelo Pydantic para la tabla proyecto_supervisor
class ProyectoSupervisor(BaseModel):
    id_proyecto: int
    id_supervisor: int

# Crear una nueva relación entre proyecto y supervisor
@appProyectoSupervisor.post("/create/", response_model=ProyectoSupervisor)
def create_proyecto_supervisor(proyecto_supervisor: ProyectoSupervisor):
    connection = get_connection()
    cursor = connection.cursor()
    #buscar por nombre de super y el folio de la soli_proyec

    cursor.execute(
        "INSERT INTO proyecto_supervisor (id_proyecto, id_supervisor) VALUES (%s, %s) RETURNING id_proyecto_supervisor",
        (proyecto_supervisor.id_proyecto, proyecto_supervisor.id_supervisor),
    )

    new_proyecto_supervisor_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**proyecto_supervisor.dict(), "id_proyecto_supervisor": new_proyecto_supervisor_id}

# Obtener una relación entre proyecto y supervisor por su ID
@appProyectoSupervisor.get("/ver/{proyecto_supervisor_id}", response_model=ProyectoSupervisor)
def get_proyecto_supervisor(proyecto_supervisor_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    # buscar por nombre de super
    cursor.execute("SELECT id_proyecto, id_supervisor FROM proyecto_supervisor WHERE id_proyecto_supervisor = %s",
                   (proyecto_supervisor_id,))
    proyecto_supervisor = cursor.fetchone()
    connection.close()

    if proyecto_supervisor is None:
        raise HTTPException(status_code=404, detail="Relación proyecto-supervisor no encontrada")

    return {"id_proyecto_supervisor": proyecto_supervisor_id, "id_proyecto": proyecto_supervisor[0],
            "id_supervisor": proyecto_supervisor[1]}

# Actualizar una relación entre proyecto y supervisor por su ID
@appProyectoSupervisor.put("/update/{proyecto_supervisor_id}", response_model=ProyectoSupervisor)
def update_proyecto_supervisor(proyecto_supervisor_id: int, proyecto_supervisor: ProyectoSupervisor):
    connection = get_connection()
    cursor = connection.cursor()
    # buscar por nombre de super
    cursor.execute(
        "UPDATE proyecto_supervisor SET id_proyecto=%s, id_supervisor=%s WHERE id_proyecto_supervisor = %s RETURNING id_proyecto_supervisor",
        (proyecto_supervisor.id_proyecto, proyecto_supervisor.id_supervisor, proyecto_supervisor_id),
    )

    updated_proyecto_supervisor_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_proyecto_supervisor_id is None:
        raise HTTPException(status_code=404, detail="Relación proyecto-supervisor no encontrada")

    return {**proyecto_supervisor.dict(), "id_proyecto_supervisor": updated_proyecto_supervisor_id}

# Eliminar una relación entre proyecto y supervisor por su ID
@appProyectoSupervisor.delete("/delete/{proyecto_supervisor_id}", response_model=dict)
def delete_proyecto_supervisor(proyecto_supervisor_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    # buscar por nombre de super
    cursor.execute("DELETE FROM proyecto_supervisor WHERE id_proyecto_supervisor = %s", (proyecto_supervisor_id,))
    connection.commit()
    connection.close()

    return {"message": "Relación proyecto-supervisor eliminada"}

# Obtener todas las relaciones entre proyecto y supervisor
@appProyectoSupervisor.get("/ver-todos/", response_model=list[ProyectoSupervisor])
def get_proyectos_supervisor():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_proyecto_supervisor, id_proyecto, id_supervisor FROM proyecto_supervisor")
    proyectos_supervisor = cursor.fetchall()
    connection.close()

    return [{"id_proyecto_supervisor": proyecto[0], "id_proyecto": proyecto[1], "id_supervisor": proyecto[2]} for proyecto in proyectos_supervisor]
