# =====================================================================
# rutas/prediccion.py · EL ENDPOINT DEL MODELO
# ---------------------------------------------------------------------
# Qué hace: define la "puerta" por la que se le pide una predicción
# al modelo:  POST /predecir
#
# Este archivo es el intermediario entre dos mundos:
#   - HTTP: recibe el JSON que manda el frontend y devuelve otro JSON
#   - Python: llama a predecir_especie(), que está en prediccion.py
# =====================================================================

# PASO 1 · Importar lo necesario
from fastapi import APIRouter              # permite definir rutas en un archivo aparte de main.py
from pydantic import BaseModel, Field      # para describir y validar los datos que llegan
from prediccion import predecir_especie    # la función que usa el modelo

# PASO 2 · Crear el router
# Es como una "mini app": acá se anotan las rutas y después main.py
# las suma a la aplicación con include_router.
router = APIRouter()


# PASO 3 · El modelo de datos: el CONTRATO de entrada
# (Ojo: acá "modelo" significa "molde de los datos", no el modelo de Machine Learning.)
# Esta clase describe qué JSON tiene que mandar el frontend: 4 números con estos nombres.
#   float     = número con decimales
#   gt=0      = "greater than 0": tiene que ser mayor que 0
#   examples  = el valor de ejemplo que se muestra en /docs
# Si falta una medida, llega texto en vez de un número o un valor negativo,
# FastAPI responde solo con un error 422 y explica qué campo está mal.
# No hace falta escribir ningún "if" para validar.
class Flor(BaseModel):
    largo_sepalo: float = Field(gt=0, examples=[5.1])
    ancho_sepalo: float = Field(gt=0, examples=[3.5])
    largo_petalo: float = Field(gt=0, examples=[1.4])
    ancho_petalo: float = Field(gt=0, examples=[0.2])


# PASO 4 · El endpoint
# Ejemplo de lo que recibe:
#   POST /predecir  {"largo_sepalo": 5.1, "ancho_sepalo": 3.5, "largo_petalo": 1.4, "ancho_petalo": 0.2}
# Ejemplo de lo que responde:
#   {"resultado": {"especie": "setosa", "probabilidades": {"setosa": 0.981, "versicolor": 0.019, "virginica": 0.0}}}
@router.post("/predecir")        # cuando llegue un POST a /predecir, ejecutar esta función
def predecir(flor: Flor):        # "flor: Flor" → FastAPI lee el JSON, lo valida y arma un objeto Flor
    return {
        "resultado": predecir_especie(   # llamamos a la lógica del modelo...
            flor.largo_sepalo,           # ...pasándole cada medida, que se lee
            flor.ancho_sepalo,           #    como un atributo del objeto flor
            flor.largo_petalo,
            flor.ancho_petalo,
        )
    }                            # FastAPI convierte este diccionario en la respuesta JSON
