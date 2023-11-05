from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appColaborador = APIRouter()

# Modelo Pydantic para la tabla colaborador
class Colaborador(BaseModel):
    id_supervisor: int
    nombre: str
    cargo: str
    telefono: int
    correo: str

# Crear un nuevo colaborador
@appColaborador.post("/create/", response_model=Colaborador)
def create_colaborador(colaborador: Colaborador):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO colaborador (id_supervisor, nombre, cargo, telefono, correo) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING id_colaborador",
        (colaborador.id_supervisor, colaborador.nombre, colaborador.cargo, colaborador.telefono, colaborador.correo),
    )

    new_colaborador_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**colaborador.dict(), "id_colaborador": new_colaborador_id}

# Obtener un colaborador por su ID
@appColaborador.get("/ver/{colaborador_id}", response_model=Colaborador)
def get_colaborador(colaborador_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_supervisor, nombre, cargo, telefono, correo FROM colaborador WHERE id_colaborador = %s",
                   (colaborador_id,))
    colaborador = cursor.fetchone()
    connection.close()

    if colaborador is None:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    return {"id_colaborador": colaborador_id, "id_supervisor": colaborador[0], "nombre": colaborador[1], "cargo": colaborador[2],
            "telefono": colaborador[3], "correo": colaborador[4]}

# Actualizar un colaborador por su ID
@appColaborador.put("/update/{colaborador_id}", response_model=Colaborador)
def update_colaborador(colaborador_id: int, colaborador: Colaborador):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE colaborador SET id_supervisor=%s, nombre=%s, cargo=%s, telefono=%s, correo=%s WHERE id_colaborador = %s RETURNING id_colaborador",
        (colaborador.id_supervisor, colaborador.nombre, colaborador.cargo, colaborador.telefono, colaborador.correo, colaborador_id),
    )

    updated_colaborador_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_colaborador_id is None:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    return {**colaborador.dict(), "id_colaborador": updated_colaborador_id}

# Eliminar un colaborador por su ID
@appColaborador.delete("/delete/{colaborador_id}", response_model=dict)
def delete_colaborador(colaborador_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM colaborador WHERE id_colaborador = %s", (colaborador_id,))
    connection.commit()
    connection.close()

    return {"message": "Colaborador eliminado"}

# Obtener todos los colaboradores
@appColaborador.get("/ver-todos/", response_model=list[Colaborador])
def get_colaboradores():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_colaborador, id_supervisor, nombre, cargo, telefono, correo FROM colaborador")
    colaboradores = cursor.fetchall()
    connection.close()

    return [{"id_colaborador": colaborador[0], "id_supervisor": colaborador[1], "nombre": colaborador[2], "cargo": colaborador[3],
            "telefono": colaborador[4], "correo": colaborador[5]} for colaborador in colaboradores]
