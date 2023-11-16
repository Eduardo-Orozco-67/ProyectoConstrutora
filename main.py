from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

# Configuración de CORS
origins = ["*"]

# Configuración de CORS Middleware
app = FastAPI(title="APIRest de Constructora S.A de C.V",
              description="Esta es una API para gestionar proyectos de una constructora.",
              version="1.0.0",
              openapi_url="/custom_openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la autenticación con JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelo para el token
class Token(BaseModel):
    access_token: str
    token_type: str

# Función para crear el token JWT
def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Base de datos de usuarios (simulada)
fake_users_db = {
    "admin": {"username": "admin", "password": "secretaacces123"},
}

# Lógica de verificación de credenciales del usuario
def verify_user_credentials(username: str, password: str):
    user = fake_users_db.get(username)
    if user and user["password"] == password:
        return True
    return False

# Función para obtener el usuario actual desde el token JWT
def get_current_user(token: str = Depends(lambda jsonwebtoken: jsonwebtoken)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

# Modelo para las credenciales del usuario en el cuerpo de la solicitud
class UserCredentialsInBody(BaseModel):
    username: str
    password: str

# Ruta para obtener el token JWT con credenciales en el cuerpo de la solicitud
@app.post("/token", response_model=Token)
async def login_for_access_token(credentials: UserCredentialsInBody):
    # Verifica las credenciales del usuario
    if verify_user_credentials(credentials.username, credentials.password):
        # Credenciales válidas, crea y devuelve el token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"access_token": create_jwt_token(data={"sub": credentials.username}, expires_delta=access_token_expires), "token_type": "bearer"}
    else:
        # Credenciales inválidas, devuelve un error 401 Unauthorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Rutas protegidas que requieren autenticación
@app.get("/protected-route", response_model=dict, dependencies=[Depends(get_current_user)])
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}

# Importación de los routers de las API
from api.empresa import appEmpresa
from api.solicitudProyecto import appSolicitudProyecto
from api.proyecto import appProyecto
from api.servicio import appServicio
from api.detalleSolicitud import appDetalleSolicitud
from api.servicioDetalleSolicitud import appServicioDetalleSolicitud
from api.supervisor import appSupervisor
from api.proyectoSupervisor import appProyectoSupervisor
from api.colaborador import appColaborador
from api.reportes import appProyectoSolicitud
from api.usuarios import appUsuarios

# Inclusión de los routers de las API
app.include_router(appEmpresa, prefix="/empresa", tags=["empresa"], dependencies=[Depends(get_current_user)])
app.include_router(appSolicitudProyecto, prefix="/solicitud_proyecto", tags=["solicitud_proyecto"], dependencies=[Depends(get_current_user)])
app.include_router(appDetalleSolicitud, prefix="/detalle_solicitud", tags=["detalle_solicitud"], dependencies=[Depends(get_current_user)])
app.include_router(appServicioDetalleSolicitud, prefix="/servicio_detalle_solicitud", tags=["servicio_detalle_solicitud"], dependencies=[Depends(get_current_user)])
app.include_router(appProyecto, prefix="/proyecto", tags=["proyecto"], dependencies=[Depends(get_current_user)])
app.include_router(appServicio, prefix="/servicio", tags=["servicio"], dependencies=[Depends(get_current_user)])
app.include_router(appSupervisor, prefix="/supervisor", tags=["supervisor"], dependencies=[Depends(get_current_user)])
app.include_router(appColaborador, prefix="/colaborador", tags=["colaborador"], dependencies=[Depends(get_current_user)])
app.include_router(appProyectoSupervisor, prefix="/proyecto_supervisor", tags=["proyecto_supervisor"], dependencies=[Depends(get_current_user)])
app.include_router(appProyectoSolicitud, prefix="/reportes", tags=["reportes"], dependencies=[Depends(get_current_user)])
app.include_router(appUsuarios, prefix="/usuarios", tags=["usuarios"])

# Inicia la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
