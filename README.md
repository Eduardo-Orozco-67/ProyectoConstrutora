# ProyectoConstrutora

# API de la constructora con FastAPI y PostgreSQL

Esta es una API REST de ejemplo para gestionar empresas utilizando FastAPI como framework web y PostgreSQL como base de datos. Proporciona operaciones CRUD (Crear, Leer, Actualizar y Eliminar) para la gestion de proyectos de una constructora.

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

Para reiniciar este proyecto

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Documentación

Documentación creada automáticamente con FastApi usando OpenAi y Swagger.

Aqui podras ver las url del api y como funcionan y que necesitan

[http://localhost:8000/docs](http://localhost:8000/docs#/default)
