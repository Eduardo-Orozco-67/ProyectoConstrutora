# ProyectoConstrutora

# API de la constructlra con FastAPI y PostgreSQL

Esta es una API REST de ejemplo para gestionar empresas utilizando FastAPI como framework web y PostgreSQL como base de datos. Proporciona operaciones CRUD (Crear, Leer, Actualizar y Eliminar) para la entidad "empresa".

## Configuración

Antes de ejecutar la API, asegúrate de tener instaladas las dependencias necesarias. Puedes instalarlas utilizando `pip` y el archivo `requirements.txt` proporcionado.

```bash
pip install -r requirements.txt
```

## Ejecutar

Para ejecutar este proyecto ejecuta el siguiente comando en tu bash o powershell con la ruta del proyecto 

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
## Rutas de la API

•POST /empresa/: Crea una nueva empresa.
•GET /empresa/{empresa_id}: Obtiene una empresa por su ID.
•PUT /empresa/{empresa_id}: Actualiza una empresa por su ID.
•DELETE /empresa/{empresa_id}: Elimina una empresa por su ID.
•GET /empresas: Obtiene una lista de todas las empresas.


