# RUTAS DEL MODELO: el endpoint para pedirle una predicción (inferencia)

from fastapi import APIRouter
from pydantic import BaseModel, Field
from prediccion import predecir_especie

router = APIRouter()


# El modelo de datos: las 4 medidas de la flor, en centímetros.
# float = número con decimales. gt=0 = tiene que ser mayor que 0.
# Si falta una medida, viene texto o un número negativo -> 422 automático.
class Flor(BaseModel):
    largo_sepalo: float = Field(gt=0, examples=[5.1])
    ancho_sepalo: float = Field(gt=0, examples=[3.5])
    largo_petalo: float = Field(gt=0, examples=[1.4])
    ancho_petalo: float = Field(gt=0, examples=[0.2])


# POST /predecir  {"largo_sepalo": 5.1, "ancho_sepalo": 3.5, "largo_petalo": 1.4, "ancho_petalo": 0.2}
@router.post("/predecir")
def predecir(flor: Flor):
    return {
        "resultado": predecir_especie(
            flor.largo_sepalo,
            flor.ancho_sepalo,
            flor.largo_petalo,
            flor.ancho_petalo,
        )
    }
