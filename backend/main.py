# ARCHIVO PRINCIPAL: crea la aplicación y le enchufa las rutas del modelo.
# Levantar el servidor (desde la carpeta backend):  uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rutas.prediccion import router as rutas_prediccion

# La aplicación
app = FastAPI(title="API del modelo Iris")


# Ruta de prueba: solo para comprobar que la API está viva
@app.get("/")
def raiz():
    return {"mensaje": "La API del modelo está funcionando"}


# CORS: permite que el frontend (en otro origen) llame a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Enchufar las rutas del modelo de Machine Learning
app.include_router(rutas_prediccion, tags=["prediccion"])
