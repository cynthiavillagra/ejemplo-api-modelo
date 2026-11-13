# =====================================================================
# main.py · EL ARCHIVO PRINCIPAL DEL BACKEND
# ---------------------------------------------------------------------
# Qué hace: crea la aplicación (la API), le configura CORS y le
# "enchufa" las rutas del modelo, que están en rutas/prediccion.py.
#
# Cómo se reparte el trabajo en el backend:
#   main.py               → arma la aplicación (este archivo)
#   rutas/prediccion.py   → define el endpoint POST /predecir
#   prediccion.py         → carga el modelo y predice (no sabe nada de HTTP)
#   modelos/              → el archivo del modelo entrenado (.joblib)
#
# Cómo se levanta el servidor (desde la carpeta backend):
#     uvicorn main:app --reload
#   main     = este archivo (main.py)
#   app      = la variable que creamos más abajo
#   --reload = reinicia el servidor solo cada vez que guardás un cambio
# =====================================================================

# PASO 1 · Importar lo necesario
from fastapi import FastAPI                               # el framework: la clase con la que se crea la API
from fastapi.middleware.cors import CORSMiddleware        # la pieza que resuelve CORS
from rutas.prediccion import router as rutas_prediccion   # las rutas del modelo, definidas en otro archivo

# PASO 2 · Crear la aplicación
# "app" es una instancia de la clase FastAPI. Todo lo demás se configura sobre ella.
# El título es el que aparece en la documentación automática (/docs).
app = FastAPI(title="API del modelo Iris")


# PASO 3 · Una ruta de prueba
# @app.get("/") es un DECORADOR: le dice a FastAPI "cuando llegue un GET a /,
# ejecutá la función de abajo". Sirve para comprobar que la API está viva
# abriendo http://localhost:8000 en el navegador.
@app.get("/")
def raiz():
    return {"mensaje": "La API del modelo está funcionando"}   # FastAPI convierte el diccionario en JSON


# PASO 3b · El chequeo de salud (health check)
# Es una convención: casi todas las APIs publicadas tienen un GET /health.
# Las plataformas en la nube (Render, Hugging Face, etc.) lo consultan cada
# tanto para saber si tu API sigue viva; si no responde, la reinician.
# No hace nada con el modelo: solo contesta "estoy bien".
@app.get("/health")
def health():
    return {"estado": "ok"}


# PASO 4 · Configurar CORS
# El navegador bloquea, por seguridad, que una página le pida datos a un
# servidor de OTRO origen (otro dominio o puerto). Nuestro frontend se abre
# con Live Server (puerto 5500) y la API está en el puerto 8000: son orígenes
# distintos. Este middleware agrega a cada respuesta los permisos necesarios.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # "*" = cualquier origen puede llamar a la API (cómodo para practicar;
                           #       al publicar conviene poner solo la dirección de tu frontend)
    allow_methods=["*"],   # se permiten todos los métodos (GET, POST, ...)
    allow_headers=["*"],   # se permiten todos los encabezados (incluye Content-Type)
)


# PASO 5 · Enchufar las rutas del modelo
# include_router suma a la app todos los endpoints definidos en rutas/prediccion.py.
# "tags" solo sirve para agruparlos bajo un título en /docs.
app.include_router(rutas_prediccion, tags=["prediccion"])
