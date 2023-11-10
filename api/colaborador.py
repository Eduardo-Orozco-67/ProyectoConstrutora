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

    try:
        # Verificar si ya existe un colaborador con el mismo teléfono o correo
        cursor.execute("SELECT id_colaborador FROM colaborador WHERE telefono = %s OR correo = %s",
                       (colaborador.telefono, colaborador.correo))
        existing_colaborador = cursor.fetchone()

        if existing_colaborador:
            raise HTTPException(status_code=400, detail="Ya existe un colaborador con el mismo teléfono o correo")

        # Insertar el nuevo colaborador
        cursor.execute(
            "INSERT INTO colaborador (id_supervisor, nombre, cargo, telefono, correo) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id_colaborador",
            (colaborador.id_supervisor, colaborador.nombre, colaborador.cargo, colaborador.telefono, colaborador.correo),
        )

        new_colaborador_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el colaborador: {str(e)}")

    finally:
        connection.close()

    return {**colaborador.dict(), "id_colaborador": new_colaborador_id}

# Eliminar un colaborador por su teléfono y correo
@appColaborador.delete("/delete/{telefono}/{correo}", response_model=dict)
def delete_colaborador(telefono: str, correo: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM colaborador WHERE telefono = %s AND correo = %s", (telefono, correo))
    connection.commit()
    connection.close()

    return {"message": "Colaborador eliminado"}

# Actualizar un colaborador por su teléfono y correo
@appColaborador.put("/update/{telefono}/{correo}", response_model=Colaborador)
def update_colaborador(telefono: str, correo: str, colaborador: Colaborador):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si existe un colaborador con el nuevo teléfono o correo
        cursor.execute("SELECT id_colaborador FROM colaborador WHERE (telefono = %s OR correo = %s) AND (telefono != %s OR correo != %s)",
                       (colaborador.telefono, colaborador.correo, telefono, correo))
        existing_colaborador = cursor.fetchone()

        if existing_colaborador:
            raise HTTPException(status_code=400, detail="Ya existe un colaborador con el mismo teléfono o correo")

        # Actualizar el colaborador
        cursor.execute(
            "UPDATE colaborador SET id_supervisor=%s, nombre=%s, cargo=%s, telefono=%s, correo=%s WHERE telefono = %s AND correo = %s RETURNING id_colaborador",
            (colaborador.id_supervisor, colaborador.nombre, colaborador.cargo, colaborador.telefono, colaborador.correo, telefono, correo),
        )

        updated_colaborador_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el colaborador: {str(e)}")

    finally:
        connection.close()

    if updated_colaborador_id is None:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    return {**colaborador.dict(), "id_colaborador": updated_colaborador_id}

# Obtener un colaborador por su teléfono y correo
# Obtener un colaborador por su teléfono y correo
@appColaborador.get("/ver1/{telefono}/{correo}", response_model=Colaborador)
def get_colaborador_ver1(telefono: int, correo: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_colaborador, id_supervisor, nombre, cargo, telefono, correo FROM colaborador WHERE telefono = %s AND correo = %s",
                   (telefono, correo))
    colaborador_data = cursor.fetchone()
    connection.close()

    if colaborador_data is None:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    return {"id_colaborador": colaborador_data[0], "id_supervisor": colaborador_data[1], "nombre": colaborador_data[2],
            "cargo": colaborador_data[3], "telefono": colaborador_data[4], "correo": colaborador_data[5]}

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
