from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection
from datetime import date

appProyectoSolicitud = APIRouter()

class SolicitudProyecto(BaseModel):
    id_solicitud: int
    id_empresa: int
    fecha: str
    monto_presupuesto: float
    monto_anticipo: float
    folio_solicitud: str
    estado: str

class DetalleSolicitud(BaseModel):
    id_detalle_solicitud: int
    id_solicitud: int
    descripcion: str
    costo: float

class ServicioDetalleSolicitud(BaseModel):
    id_servicio_detalle_solicitud: int
    id_detalle_solicitud: int
    id_servicio: int

class Servicio(BaseModel):
    id_servicio: int
    servicio: str
    descripcion: str

class ProyectoSolicitudServicio(BaseModel):
    servicio: str
    descripcion_servicio: str

class ProyectoSolicitud(BaseModel):
    nombre_empresa: str
    id_solicitud: int
    id_empresa: int
    fecha: date
    monto_presupuesto: int
    monto_anticipo: int
    folio_solicitud: str
    estado: str
    descripcion_solicitud: str
    costo_solicitud: int
    servicios: list[ProyectoSolicitudServicio]

class ProyectoSolicitud2(BaseModel):
    nombre_empresa: str
    id_solicitud: int
    id_empresa: int
    fecha: date
    monto_presupuesto: int
    monto_anticipo: int
    folio_solicitud: str
    estado: str
    descripcion_solicitud: str
    costo_solicitud: int

@appProyectoSolicitud.get("/proyectos-50/", response_model=list[ProyectoSolicitud2])
def get_proyectos_solicitud():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT e.nombre as nombre_empresa, sp.*, ds.descripcion as descripcion_solicitud, ds.costo as costo_solicitud "
        "FROM proyecto p "
        "INNER JOIN solicitud_proyecto sp ON p.id_solicitud = sp.id_solicitud "
        "INNER JOIN empresa e ON sp.id_empresa = e.id_empresa "
        "INNER JOIN detalle_solicitud ds ON sp.id_solicitud = ds.id_solicitud "
        "WHERE p.porcentaje_avance > 49;"
    )

    proyectos_solicitud = cursor.fetchall()
    connection.close()

    proyectos_solicitud_list = []

    for proyecto in proyectos_solicitud:
        proyectos_solicitud_list.append({
            "nombre_empresa": proyecto[0],
            "id_solicitud": proyecto[1],
            "id_empresa": proyecto[2],
            "fecha": proyecto[3],
            "monto_presupuesto": proyecto[4],
            "monto_anticipo": proyecto[5],
            "folio_solicitud": proyecto[6],
            "estado": proyecto[7],
            "descripcion_solicitud": proyecto[8],
            "costo_solicitud": proyecto[9]
        })

    return proyectos_solicitud_list

@appProyectoSolicitud.get("/proyectos-aceptados/", response_model=list[ProyectoSolicitud])
def get_proyectos_solicitud():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT e.nombre as nombre_empresa, sp.*, ds.descripcion as descripcion_solicitud, ds.costo as costo_solicitud, s.servicio, s.descripcion as descripcion_servicio "
        "FROM proyecto p "
        "INNER JOIN solicitud_proyecto sp ON p.id_solicitud = sp.id_solicitud "
        "INNER JOIN empresa e ON sp.id_empresa = e.id_empresa "
        "INNER JOIN detalle_solicitud ds ON sp.id_solicitud = ds.id_solicitud "
        "LEFT JOIN servicio_detalle_solicitud sds ON ds.id_detalle_solicitud = sds.id_detalle_solicitud "
        "LEFT JOIN servicio s ON sds.id_servicio = s.id_servicio "
        ";"
    )

    proyectos_solicitud = cursor.fetchall()
    connection.close()

    proyectos_solicitud_list = []
    current_proyecto = None

    for proyecto in proyectos_solicitud:
        # Si cambiamos de proyecto, creamos uno nuevo
        if current_proyecto is None or current_proyecto['id_solicitud'] != proyecto[1]:
            if current_proyecto is not None:
                proyectos_solicitud_list.append(current_proyecto)
            current_proyecto = {
                "nombre_empresa": proyecto[0],
                "id_solicitud": proyecto[1],
                "id_empresa": proyecto[2],
                "fecha": proyecto[3],
                "monto_presupuesto": proyecto[4],
                "monto_anticipo": proyecto[5],
                "folio_solicitud": proyecto[6],
                "estado": proyecto[7],
                "descripcion_solicitud": proyecto[8],
                "costo_solicitud": proyecto[9],
                "servicios": []
            }

        # Agregamos información de servicios si existe
        if proyecto[10] is not None:
            current_proyecto['servicios'].append({
                "servicio": proyecto[10],
                "descripcion_servicio": proyecto[11]
            })

    # Añadimos el último proyecto a la lista
    if current_proyecto is not None:
        proyectos_solicitud_list.append(current_proyecto)

    return proyectos_solicitud_list

@appProyectoSolicitud.get("/proyectos-prioridad/", response_model=list[ProyectoSolicitud])
def get_proyectos_solicitud():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT e.nombre as nombre_empresa, sp.*, ds.descripcion as descripcion_solicitud, ds.costo as costo_solicitud, s.servicio, s.descripcion as descripcion_servicio "
        "FROM proyecto p "
        "INNER JOIN solicitud_proyecto sp ON p.id_solicitud = sp.id_solicitud "
        "INNER JOIN empresa e ON sp.id_empresa = e.id_empresa "
        "INNER JOIN detalle_solicitud ds ON sp.id_solicitud = ds.id_solicitud "
        "LEFT JOIN servicio_detalle_solicitud sds ON ds.id_detalle_solicitud = sds.id_detalle_solicitud "
        "LEFT JOIN servicio s ON sds.id_servicio = s.id_servicio "
        "WHERE p.prioridad = 'alta';"
    )

    proyectos_solicitud = cursor.fetchall()
    connection.close()

    proyectos_solicitud_list = []
    current_proyecto = None

    for proyecto in proyectos_solicitud:
        # Si cambiamos de proyecto, creamos uno nuevo
        if current_proyecto is None or current_proyecto['id_solicitud'] != proyecto[1]:
            if current_proyecto is not None:
                proyectos_solicitud_list.append(current_proyecto)
            current_proyecto = {
                "nombre_empresa": proyecto[0],
                "id_solicitud": proyecto[1],
                "id_empresa": proyecto[2],
                "fecha": proyecto[3],
                "monto_presupuesto": proyecto[4],
                "monto_anticipo": proyecto[5],
                "folio_solicitud": proyecto[6],
                "estado": proyecto[7],
                "descripcion_solicitud": proyecto[8],
                "costo_solicitud": proyecto[9],
                "servicios": []
            }

        # Agregamos información de servicios si existe
        if proyecto[10] is not None:
            current_proyecto['servicios'].append({
                "servicio": proyecto[10],
                "descripcion_servicio": proyecto[11]
            })

    # Añadimos el último proyecto a la lista
    if current_proyecto is not None:
        proyectos_solicitud_list.append(current_proyecto)

    return proyectos_solicitud_list