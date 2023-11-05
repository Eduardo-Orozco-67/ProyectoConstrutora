from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appProyecto = APIRouter()

# Modelo Pydantic para la tabla proyecto
class Proyecto(BaseModel):
    id_empresa: int
    id_solicitud: int
    fecha_inicio: str
    fecha_fin: str
    monto: float
    prioridad: str
    porcentaje_avance: float
    estado_proyecto: str

# Crear un nuevo proyecto
@appProyecto.post("/create/", response_model=Proyecto)
def create_proyecto(proyecto: Proyecto):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO proyecto (id_empresa, id_solicitud, fecha_inicio, fecha_fin, monto, prioridad, porcentaje_avance, estado_proyecto) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_proyecto",
        (proyecto.id_empresa, proyecto.id_solicitud, proyecto.fecha_inicio, proyecto.fecha_fin,
         proyecto.monto, proyecto.prioridad, proyecto.porcentaje_avance, proyecto.estado_proyecto),
    )

    new_proyecto_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**proyecto.dict(), "id_proyecto": new_proyecto_id}

# Obtener un proyecto por su ID
@appProyecto.get("/ver1/{proyecto_id}", response_model=Proyecto)
def get_proyecto(proyecto_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_proyecto, id_empresa, id_solicitud, fecha_inicio, fecha_fin, monto, prioridad, porcentaje_avance, estado_proyecto "
                   "FROM proyecto WHERE id_proyecto = %s", (proyecto_id,))
    proyecto = cursor.fetchone()
    connection.close()

    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    return {"id_proyecto": proyecto[0], "id_empresa": proyecto[1], "id_solicitud": proyecto[2], "fecha_inicio": proyecto[3],
            "fecha_fin": proyecto[4], "monto": proyecto[5], "prioridad": proyecto[6], "porcentaje_avance": proyecto[7],
            "estado_proyecto": proyecto[8]}

# Actualizar un proyecto por su ID
@appProyecto.put("/update/{proyecto_id}", response_model=Proyecto)
def update_proyecto(proyecto_id: int, proyecto: Proyecto):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE proyecto SET id_empresa=%s, id_solicitud=%s, fecha_inicio=%s, fecha_fin=%s, monto=%s, prioridad=%s, porcentaje_avance=%s, estado_proyecto=%s "
        "WHERE id_proyecto = %s RETURNING id_proyecto",
        (proyecto.id_empresa, proyecto.id_solicitud, proyecto.fecha_inicio, proyecto.fecha_fin, proyecto.monto,
         proyecto.prioridad, proyecto.porcentaje_avance, proyecto.estado_proyecto, proyecto_id),
    )

    updated_proyecto_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_proyecto_id is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    return {**proyecto.dict(), "id_proyecto": updated_proyecto_id}

# Eliminar un proyecto por su ID
@appProyecto.delete("/delete/{proyecto_id}", response_model=dict)
def delete_proyecto(proyecto_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM proyecto WHERE id_proyecto = %s", (proyecto_id,))
    connection.commit()
    connection.close()

    return {"message": "Proyecto eliminado"}

# Obtener todos los proyectos
@appProyecto.get("/ver-todos", response_model=list[Proyecto])
def get_proyectos():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_proyecto, id_empresa, id_solicitud, fecha_inicio, fecha_fin, monto, prioridad, porcentaje_avance, estado_proyecto "
                   "FROM proyecto")
    proyectos = cursor.fetchall()
    connection.close()

    return [{"id_proyecto": proyecto[0], "id_empresa": proyecto[1], "id_solicitud": proyecto[2], "fecha_inicio": proyecto[3],
            "fecha_fin": proyecto[4], "monto": proyecto[5], "prioridad": proyecto[6], "porcentaje_avance": proyecto[7],
            "estado_proyecto": proyecto[8]} for proyecto in proyectos]
