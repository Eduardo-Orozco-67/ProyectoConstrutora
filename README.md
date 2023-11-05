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

# Rutas de la API

## 1. API Empresa

### - POST /empresa/create/
Crea una nueva empresa.

### - GET /empresa/ver1/{empresa_id}
Obtiene una empresa por su ID.

### - PUT /empresa/update/{empresa_id}
Actualiza una empresa por su ID.

### - DELETE /empresa/delete/{empresa_id}
Elimina una empresa por su ID.

### - GET /empresas/ver-todas/
Obtiene una lista de todas las empresas.

## 2. API Solicitud de Proyecto

### - POST /solicitud_proyecto/create/
Crea una nueva solicitud de proyecto.

### - GET /solicitud_proyecto/ver1/{solicitud_id}
Obtiene una solicitud de proyecto por su ID.

### - PUT /solicitud_proyecto/update/{solicitud_id}
Actualiza una solicitud de proyecto por su ID.

### - DELETE /solicitud_proyecto/delete/{solicitud_id}
Elimina una solicitud de proyecto por su ID.

### - GET /solicitudes_proyecto/ver-todas/
Obtiene una lista de todas las solicitudes de proyecto.

## 3. API Proyecto

### - POST /proyecto/create/
Crea un nuevo proyecto.

### - GET /proyecto/ver1/{proyecto_id}
Obtiene un proyecto por su ID.

### - PUT /proyecto/update/{proyecto_id}
Actualiza un proyecto por su ID.

### - DELETE /proyecto/delete/{proyecto_id}
Elimina un proyecto por su ID.

### - GET /proyectos/ver-todos/
Obtiene una lista de todos los proyectos.

## 4. API Servicio

### - POST /servicio/create/
Crea un nuevo servicio.

### - GET /servicio/ver1/{servicio_id}
Obtiene un servicio por su ID.

### - PUT /servicio/update/{servicio_id}
Actualiza un servicio por su ID.

### - DELETE /servicio/delete/{servicio_id}
Elimina un servicio por su ID.

### - GET /servicios/ver-todos/
Obtiene una lista de todos los servicios.

## 5. API Detalle de Solicitud

### - POST /detalle_solicitud/create/
Crea un nuevo detalle de solicitud.

### - GET /detalle_solicitud/ver1/{detalle_solicitud_id}
Obtiene un detalle de solicitud por su ID.

### - PUT /detalle_solicitud/update/{detalle_solicitud_id}
Actualiza un detalle de solicitud por su ID.

### - DELETE /detalle_solicitud/delete/{detalle_solicitud_id}
Elimina un detalle de solicitud por su ID.

### - GET /detalles_solicitud/ver-todos/
Obtiene una lista de todos los detalles de solicitud.

## 6. API Servicio Detalle de Solicitud

### - POST /servicio_detalle_solicitud/create/
Crea un nuevo registro de servicio en detalle de solicitud.

### - GET /servicio_detalle_solicitud/ver1/{servicio_detalle_solicitud_id}
Obtiene un registro de servicio en detalle de solicitud por su ID.

### - PUT /servicio_detalle_solicitud/update/{servicio_detalle_solicitud_id}
Actualiza un registro de servicio en detalle de solicitud por su ID.

### - DELETE /servicio_detalle_solicitud/delete/{servicio_detalle_solicitud_id}
Elimina un registro de servicio en detalle de solicitud por su ID.

### - GET /servicios_detalle_solicitud/ver-todos/
Obtiene una lista de todos los registros de servicios en detalles de solicitud.

## 7. API Supervisor

### - POST /supervisor/create/
Crea un nuevo supervisor.

### - GET /supervisor/ver1/{supervisor_id}
Obtiene un supervisor por su ID.

### - PUT /supervisor/update/{supervisor_id}
Actualiza un supervisor por su ID.

### - DELETE /supervisor/delete/{supervisor_id}
Elimina un supervisor por su ID.

### - GET /supervisores/ver-todos/
Obtiene una lista de todos los supervisores.

## 8. API Proyecto Supervisor

### - POST /proyecto_supervisor/create/
Crea un nuevo registro de proyecto-supervisor.

### - GET /proyecto_supervisor/ver1/{proyecto_supervisor_id}
Obtiene un registro de proyecto-supervisor por su ID.

### - PUT /proyecto_supervisor/update/{proyecto_supervisor_id}
Actualiza un registro de proyecto-supervisor por su ID.

### - DELETE /proyecto_supervisor/delete/{proyecto_supervisor_id}
Elimina un registro de proyecto-supervisor por su ID.

### - GET /proyectos_supervisor/ver-todos/
Obtiene una lista de todos los registros de proyecto-supervisor.

## 9. API Colaborador

### - POST /colaborador/create/
Crea un nuevo colaborador.

### - GET /colaborador/ver1/{colaborador_id}
Obtiene un colaborador por su ID.

### - PUT /colaborador/update/{colaborador_id}
Actualiza un colaborador por su ID.

### - DELETE /colaborador/delete/{colaborador_id}
Elimina un colaborador por su ID.

### - GET /colaboradores/ver-todos/
Obtiene una lista de todos los colaboradores.

## Documentación

Documentación cread automáticamente con FastApi usando OpenAoi y Swagger

[http://localhost:8000/docs](http://localhost:8000/docs#/default)
