###importamos fastApi para crear la aplicacion
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

##importamos los archivos que tienen los endpoints
from api.empresa import appEmpresa
from api.solicitudProyecto import appSolicitudProyecto
from api.proyecto import appProyecto
from api.servicio import appServicio
from api.detalleSolicitud import appDetalleSolicitud
from api.servicioDetalleSolicitud import appServicioDetalleSolicitud
from api.supervisor import appSupervisor
from api.proyectoSupervisor import appProyectoSupervisor
from api.colaborador import appColaborador

###para configurar swagger openapi

### FastAPI incluye documentacion con Swagger y OpenAPI de forma automatica solo configuramos estos parametros
app = FastAPI(title="APIRest de Constructora S.A de C.V",
    description="Esta es una API para gestionar proyectos de una constructora.",
    version="1.0.0",
    openapi_url="/custom_openapi.json" )

# Configuración de CORS para permitir solicitudes desde 'http://localhost:5173'
origins = [
    "http://localhost:5173",  # Agrega aquí el origen de tu aplicación cliente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


###incluimos los router de las api
app.include_router(appEmpresa, prefix="/empresa", tags=["empresa"])
app.include_router(appSolicitudProyecto, prefix="/solicitud_proyecto", tags=["solicitud_proyecto"])
app.include_router(appProyecto, prefix="/proyecto", tags=["proyecto"])
app.include_router(appServicio, prefix="/servicio", tags=["servicio"])
app.include_router(appDetalleSolicitud, prefix="/detalle_solicitud", tags=["detalle_solicitud"])
app.include_router(appServicioDetalleSolicitud, prefix="/servicio_detalle_solicitud", tags=["servicio_detalle_solicitud"])
app.include_router(appSupervisor, prefix="/supervisor", tags=["supervisor"])
app.include_router(appProyectoSupervisor, prefix="/proyecto_supervisor", tags=["proyecto_supervisor"])
app.include_router(appColaborador, prefix="/colaborador", tags=["colaborador"])

#localhost:8000/prefijo/metodo(get, update, etc)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)