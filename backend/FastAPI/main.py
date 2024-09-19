from fastapi import FastAPI

app = FastAPI()


@app.get("/saludo")
async def root():
    """
    Función que retorna un mensaje
    """
    return {"message": "Hello World"}


@app.get("/")
async def root():
    return "Hola FastAPI!"


@app.get("/url")
async def url():
    return {"url_curso": "https://youtube.com"}


# Url local: http://127.0.0.1:8000
# Iniciando el servidor: uvicorn main:app --reload

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
