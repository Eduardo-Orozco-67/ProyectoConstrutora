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

# Crear un nuevo supervisor
@appSupervisor.post("/create/", response_model=Supervisor)
def create_supervisor(supervisor: Supervisor):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO supervisor (nombre, cargo, telefono, correo) VALUES (%s, %s, %s, %s) RETURNING id_supervisor",
        (supervisor.nombre, supervisor.cargo, supervisor.telefono, supervisor.correo),
    )

    new_supervisor_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return {**supervisor.dict(), "id_supervisor": new_supervisor_id}

# Obtener un supervisor por su ID
@appSupervisor.get("/ver/{supervisor_id}", response_model=Supervisor)
def get_supervisor(supervisor_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT nombre, cargo, telefono, correo FROM supervisor WHERE id_supervisor = %s", (supervisor_id,))
    supervisor = cursor.fetchone()
    connection.close()

    if supervisor is None:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado")

    return {"id_supervisor": supervisor_id, "nombre": supervisor[0], "cargo": supervisor[1], "telefono": supervisor[2], "correo": supervisor[3]}

# Actualizar un supervisor por su ID
@appSupervisor.put("/update/{supervisor_id}", response_model=Supervisor)
def update_supervisor(supervisor_id: int, supervisor: Supervisor):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE supervisor SET nombre=%s, cargo=%s, telefono=%s, correo=%s WHERE id_supervisor = %s RETURNING id_supervisor",
        (supervisor.nombre, supervisor.cargo, supervisor.telefono, supervisor.correo, supervisor_id),
    )

    updated_supervisor_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if updated_supervisor_id is None:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado")

    return {**supervisor.dict(), "id_supervisor": updated_supervisor_id}

# Eliminar un supervisor por su ID
@appSupervisor.delete("/delete/{supervisor_id}", response_model=dict)
def delete_supervisor(supervisor_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM supervisor WHERE id_supervisor = %s", (supervisor_id,))
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
