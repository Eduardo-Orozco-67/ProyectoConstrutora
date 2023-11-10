from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conexion.db import get_connection

appSupervisor = APIRouter()

# Modelo Pydantic para la tabla supervisor
class Supervisor(BaseModel):
    nombre: str
    cargo: str
    telefono: int
    correo: str

# Crear un supervisor
@appSupervisor.post("/create/", response_model=Supervisor)
def create_supervisor(supervisor: Supervisor):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si ya existe un supervisor con el mismo teléfono o correo
        cursor.execute("SELECT id_supervisor FROM supervisor WHERE telefono = %s OR correo = %s",
                       (supervisor.telefono, supervisor.correo))
        existing_supervisor = cursor.fetchone()

        if existing_supervisor:
            raise HTTPException(status_code=400, detail="Ya existe un supervisor con el mismo teléfono o correo")

        # Insertar el nuevo supervisor
        cursor.execute(
            "INSERT INTO supervisor (nombre, cargo, telefono, correo) VALUES (%s, %s, %s, %s) RETURNING id_supervisor",
            (supervisor.nombre, supervisor.cargo, supervisor.telefono, supervisor.correo),
        )

        new_supervisor_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el supervisor: {str(e)}")

    finally:
        connection.close()

    return {**supervisor.dict(), "id_supervisor": new_supervisor_id}

# Obtener un supervisor por su ID
@appSupervisor.get("/ver1/{telefono}/{correo}", response_model=Supervisor)
def get_supervisor(telefono: int, correo: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_supervisor, nombre, cargo FROM supervisor WHERE telefono = %s AND correo = %s", (telefono, correo))
    supervisor = cursor.fetchone()
    connection.close()

    if supervisor is None:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado")

    return {"id_supervisor": supervisor[0], "nombre": supervisor[1], "cargo": supervisor[2], "telefono": telefono, "correo": correo}

# Actualizar un supervisor por su teléfono y correo
@appSupervisor.put("/update/{telefono}/{correo}", response_model=Supervisor)
def update_supervisor(telefono: str, correo: str, supervisor: Supervisor):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si existe un supervisor con el nuevo teléfono o correo
        cursor.execute("SELECT id_supervisor FROM supervisor WHERE (telefono = %s OR correo = %s) AND (telefono != %s OR correo != %s)",
                       (supervisor.telefono, supervisor.correo, telefono, correo))
        existing_supervisor = cursor.fetchone()

        if existing_supervisor:
            raise HTTPException(status_code=400, detail="Ya existe un supervisor con el mismo teléfono o correo")

        # Actualizar el supervisor
        cursor.execute(
            "UPDATE supervisor SET nombre=%s, cargo=%s, telefono=%s, correo=%s WHERE telefono = %s AND correo = %s RETURNING id_supervisor",
            (supervisor.nombre, supervisor.cargo, supervisor.telefono, supervisor.correo, telefono, correo),
        )

        updated_supervisor_id = cursor.fetchone()[0]
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el supervisor: {str(e)}")

    finally:
        connection.close()

    return {**supervisor.dict(), "id_supervisor": updated_supervisor_id}

# Eliminar un supervisor por su teléfono y correo
@appSupervisor.delete("/delete/{telefono}/{correo}", response_model=dict)
def delete_supervisor(telefono: str, correo: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM supervisor WHERE telefono = %s AND correo = %s", (telefono, correo))
    connection.commit()
    connection.close()

    return {"message": "Supervisor eliminado"}

# Obtener todos los supervisores
@appSupervisor.get("/ver-todos/", response_model=list[Supervisor])
def get_supervisores():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id_supervisor, nombre, cargo, telefono, correo FROM supervisor")
    supervisores = cursor.fetchall()
    connection.close()

    return [{"id_supervisor": supervisor[0], "nombre": supervisor[1], "cargo": supervisor[2], "telefono": supervisor[3], "correo": supervisor[4]} for supervisor in supervisores]
