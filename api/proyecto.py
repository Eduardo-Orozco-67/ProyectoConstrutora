from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection
from datetime import datetime


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

class ProyectoSearch(BaseModel):
    id_proyecto: int
    empresa: str
    folio_solicitud: str
    fecha_inicio: str
    fecha_fin: str
    monto: float
    prioridad: str
    porcentaje_avance: float
    estado_proyecto: str

class ProyectoCreate(BaseModel):
    fecha_inicio: str
    fecha_fin: str
    prioridad: str
    folio_solicitud: str


# Crear un nuevo proyecto
# Crear un proyecto aceptadO
@appProyecto.post("/create/", response_model=ProyectoCreate)
def create_proyecto(fecha_inicio: str, fecha_fin: str, prioridad: str, folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si la solicitud ya tiene un proyecto asociado
        cursor.execute("SELECT id_proyecto FROM proyecto WHERE id_solicitud = (SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s)", (folio_solicitud,))
        existing_proyecto = cursor.fetchone()

        if existing_proyecto:
            raise HTTPException(status_code=400, detail="Ya existe un proyecto asociado a esta solicitud")

        # Llamar al procedimiento almacenado y obtener el resultado
        cursor.execute("CALL guardar_proyecto_aceptado(%s, %s, %s, %s, NULL, NULL)",
                       (fecha_inicio, fecha_fin, prioridad, folio_solicitud))

        # Obtener el resultado del procedimiento almacenado (pRes)
        pRes = cursor.fetchone()
        print(f"pRes: {pRes[0]}")
        # Commitear la transacción si todo salió bien
        connection.commit()

        # Verificar el resultado del procedimiento almacenado
        if pRes[0] == 1:
            # Cerrar la conexión y devolver un proyecto vacío (o algún otro indicador de éxito)
            connection.close()
            return ProyectoCreate(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                prioridad=prioridad,
                folio_solicitud=folio_solicitud
            )
        else:
            # Si hay un error, lanzar una excepción con el código de error
            raise HTTPException(status_code=500, detail=f"Error al crear el proyecto. fechas erroneas, folio incorrecto, la solicitud esta rechazada/pendiente o ese folio ya fue regsitrado")

    except Exception as e:
        # En caso de error, hacer rollback y lanzar excepción
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el proyecto. fechas erroneas, folio incorrecto, la solicitud esta rechazada/pendiente o ese folio ya fue registrado")

    finally:
        # Siempre cerrar la conexión al final
        connection.close()

# Obtener un proyecto por su folio_solicitud
@appProyecto.get("/ver1/{folio_solicitud}", response_model=ProyectoSearch)
def get_proyecto(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Realizar un INNER JOIN con la tabla empresa para obtener el nombre de la empresa
        cursor.execute(
            "SELECT p.id_proyecto, e.nombre, s.id_solicitud, p.fecha_inicio, p.fecha_fin, p.monto, p.prioridad, p.porcentaje_avance, p.estado_proyecto "
            "FROM proyecto p "
            "INNER JOIN solicitud_proyecto s ON p.id_solicitud = s.id_solicitud "
            "INNER JOIN empresa e ON p.id_empresa = e.id_empresa "
            "WHERE s.folio_solicitud = %s",
            (folio_solicitud,),
        )

        proyecto = cursor.fetchone()

        if proyecto is None:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    except HTTPException as e:
        raise e  # Ya es una excepción HTTP, solo regrésala
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el proyecto: {str(e)}")
    finally:
        connection.close()

    # Usa strftime directamente en los objetos date
    fecha_inicio_str = proyecto[3].strftime("%d/%m/%Y")
    fecha_fin_str = proyecto[4].strftime("%d/%m/%Y")

    return ProyectoSearch(
        id_proyecto=proyecto[0],
        empresa=proyecto[1],
        folio_solicitud=folio_solicitud,
        fecha_inicio=fecha_inicio_str,
        fecha_fin=fecha_fin_str,
        monto=proyecto[5],
        prioridad=proyecto[6],
        porcentaje_avance=proyecto[7],
        estado_proyecto=proyecto[8]
    )


# Actualizar un proyecto por su ID
# Actualizar un proyecto por su folio_solicitud
@appProyecto.put("/update/{folio_solicitud}", response_model=Proyecto)
def update_proyecto(folio_solicitud: str, proyecto: Proyecto):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Buscar el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud = id_solicitud[0]
        print(f"{id_solicitud}")

        # Convertir las fechas al formato correcto
        fecha_inicio = datetime.strptime(proyecto.fecha_inicio, "%d/%m/%Y").date()
        fecha_fin = datetime.strptime(proyecto.fecha_fin, "%d/%m/%Y").date()

        # Actualizar el proyecto por id_solicitud
        cursor.execute(
            "UPDATE proyecto SET id_empresa=%s, id_solicitud=%s, fecha_inicio=%s, fecha_fin=%s, monto=%s, prioridad=%s, porcentaje_avance=%s, estado_proyecto=%s "
            "WHERE id_solicitud = %s RETURNING id_proyecto",
            (proyecto.id_empresa, id_solicitud, fecha_inicio, fecha_fin,
             proyecto.monto, proyecto.prioridad, proyecto.porcentaje_avance, proyecto.estado_proyecto, id_solicitud),
        )

        updated_proyecto_row = cursor.fetchone()

        if updated_proyecto_row:
            updated_proyecto_id = updated_proyecto_row[0]
            connection.commit()
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar el proyecto: No se obtuvo ninguna fila después de la actualización")
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el proyecto: {str(e)}")
    finally:
        connection.close()

    return {**proyecto.dict(), "id_proyecto": updated_proyecto_id}



# Definir el endpoint para actualizar el porcentaje de avance
@appProyecto.patch("/update-porcentaje/{folio_solicitud}", response_model=dict)
def update_porcentaje_avance(folio_solicitud: str, porcentaje_avance: float):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud = id_solicitud[0]

        # Actualizar el porcentaje de avance
        cursor.execute(
            "UPDATE proyecto SET porcentaje_avance = %s WHERE id_solicitud = %s RETURNING porcentaje_avance",
            (porcentaje_avance, id_solicitud),
        )

        updated_porcentaje_avance = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el porcentaje de avance: {str(e)}")

    finally:
        connection.close()

    return {"porcentaje_avance": updated_porcentaje_avance}

# modificar el estado entre terminado y en proceso
@appProyecto.patch("/update-estado/{folio_solicitud}", response_model=dict)
def update_estado_proyecto(folio_solicitud: str, estado_proyecto: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Obtener el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud = id_solicitud[0]

        # Actualizar el estado del proyecto
        cursor.execute(
            "UPDATE proyecto SET estado_proyecto = %s WHERE id_solicitud = %s RETURNING estado_proyecto",
            (estado_proyecto, id_solicitud),
        )

        updated_estado_proyecto = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado del proyecto: {str(e)}")

    finally:
        connection.close()

    return {"estado_proyecto": updated_estado_proyecto}


# Eliminar un proyecto por su folio_solicitud
@appProyecto.delete("/delete/{folio_solicitud}", response_model=dict)
def delete_proyecto(folio_solicitud: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Buscar el id_solicitud correspondiente al folio_solicitud
        cursor.execute("SELECT id_solicitud FROM solicitud_proyecto WHERE folio_solicitud = %s", (folio_solicitud,))
        id_solicitud = cursor.fetchone()

        if id_solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud de proyecto no encontrada")

        id_solicitud = id_solicitud[0]

        # Eliminar el proyecto por id_solicitud
        cursor.execute("DELETE FROM proyecto WHERE id_solicitud = %s", (id_solicitud,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el proyecto: {str(e)}")
    finally:
        connection.close()

    return {"message": "Proyecto eliminado"}

# ver todos los proyectos
@appProyecto.get("/ver-todos", response_model=list[ProyectoSearch])
def get_all_proyectos():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Realizar un INNER JOIN con la tabla empresa para obtener el nombre de la empresa
        cursor.execute(
            "SELECT p.id_proyecto, e.nombre, s.folio_solicitud, p.fecha_inicio, p.fecha_fin, p.monto, p.prioridad, p.porcentaje_avance, p.estado_proyecto "
            "FROM proyecto p "
            "INNER JOIN solicitud_proyecto s ON p.id_solicitud = s.id_solicitud "
            "INNER JOIN empresa e ON p.id_empresa = e.id_empresa"
        )

        proyectos = cursor.fetchall()

        # Convertir los resultados a objetos ProyectoSearch
        proyectos_list = []
        for proyecto_row in proyectos:
            proyecto_data = ProyectoSearch(
                id_proyecto=proyecto_row[0],
                empresa=proyecto_row[1],
                folio_solicitud=proyecto_row[2],
                fecha_inicio=proyecto_row[3].strftime("%d/%m/%Y"),
                fecha_fin=proyecto_row[4].strftime("%d/%m/%Y"),
                monto=proyecto_row[5],
                prioridad=proyecto_row[6],
                porcentaje_avance=proyecto_row[7],
                estado_proyecto=proyecto_row[8],
            )
            proyectos_list.append(proyecto_data)

        return proyectos_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos: {str(e)}")
    finally:
        connection.close()

@appProyecto.get("/ver-por-prioridad", response_model=list[ProyectoSearch])
def get_proyectos_by_prioridad(prioridad: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Realizar un INNER JOIN con la tabla empresa para obtener el nombre de la empresa
        cursor.execute(
            "SELECT p.id_proyecto, e.nombre, s.folio_solicitud, p.fecha_inicio, p.fecha_fin, p.monto, p.prioridad, p.porcentaje_avance, p.estado_proyecto "
            "FROM proyecto p "
            "INNER JOIN solicitud_proyecto s ON p.id_solicitud = s.id_solicitud "
            "INNER JOIN empresa e ON p.id_empresa = e.id_empresa "
            "WHERE p.prioridad = %s",
            (prioridad,)
        )

        proyectos = cursor.fetchall()

        # Convertir los resultados a objetos ProyectoSearch
        proyectos_list = []
        for proyecto_row in proyectos:
            proyecto_data = ProyectoSearch(
                id_proyecto=proyecto_row[0],
                empresa=proyecto_row[1],
                folio_solicitud=proyecto_row[2],
                fecha_inicio=proyecto_row[3].strftime("%d/%m/%Y"),
                fecha_fin=proyecto_row[4].strftime("%d/%m/%Y"),
                monto=proyecto_row[5],
                prioridad=proyecto_row[6],
                porcentaje_avance=proyecto_row[7],
                estado_proyecto=proyecto_row[8],
            )
            proyectos_list.append(proyecto_data)

        return proyectos_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos por prioridad: {str(e)}")
    finally:
        connection.close()

@appProyecto.get("/ver-por-estado", response_model=list[ProyectoSearch])
def get_proyectos_by_estado(estado_proyecto: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Realizar un INNER JOIN con la tabla empresa para obtener el nombre de la empresa
        cursor.execute(
            "SELECT p.id_proyecto, e.nombre, s.folio_solicitud, p.fecha_inicio, p.fecha_fin, p.monto, p.prioridad, p.porcentaje_avance, p.estado_proyecto "
            "FROM proyecto p "
            "INNER JOIN solicitud_proyecto s ON p.id_solicitud = s.id_solicitud "
            "INNER JOIN empresa e ON p.id_empresa = e.id_empresa "
            "WHERE p.estado_proyecto = %s",
            (estado_proyecto,)
        )

        proyectos = cursor.fetchall()

        # Convertir los resultados a objetos ProyectoSearch
        proyectos_list = []
        for proyecto_row in proyectos:
            proyecto_data = ProyectoSearch(
                id_proyecto=proyecto_row[0],
                empresa=proyecto_row[1],
                folio_solicitud=proyecto_row[2],
                fecha_inicio=proyecto_row[3].strftime("%d/%m/%Y"),
                fecha_fin=proyecto_row[4].strftime("%d/%m/%Y"),
                monto=proyecto_row[5],
                prioridad=proyecto_row[6],
                porcentaje_avance=proyecto_row[7],
                estado_proyecto=proyecto_row[8],
            )
            proyectos_list.append(proyecto_data)

        return proyectos_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos por estado: {str(e)}")
    finally:
        connection.close()
