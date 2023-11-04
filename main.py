from fastapi import FastAPI
from api import app
from config import openapi_config

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
