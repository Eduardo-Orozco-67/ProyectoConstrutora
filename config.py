from fastapi.openapi.models import OAuthFlows
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlowAuthorizationCode as OAuthFlowAuthorizationCodeModel

openapi_config = {
    "openapi": "3.0.2",
    "info": {
        "title": "API de Empresas",
        "version": "1.0"
    },
    "security": [
        {
            "oauth2PasswordBearer": []
        }
    ],
    "servers": [
        {
            "url": "http://localhost:8000/config"
        }
    ],
    "oauth2PasswordBearer": {
        "tokenUrl": "/token",
        "flow": "password",
    },
}
