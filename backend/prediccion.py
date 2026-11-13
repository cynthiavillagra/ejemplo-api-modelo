# =====================================================================
# prediccion.py · LA LÓGICA DEL MODELO
# ---------------------------------------------------------------------
# Qué hace: carga el modelo entrenado y predice la especie de una flor.
# Este archivo NO sabe nada de HTTP ni de FastAPI: es Python puro.
# (Cumple el mismo papel que appV2.py en el ejemplo de los nombres.)
#
# Esa separación es a propósito: la API (rutas/prediccion.py) solo
# recibe el pedido y llama a la función de este archivo.
#
# Para probar solo el modelo, sin la API: sacale el "#" a las dos
# últimas líneas y corré   python prediccion.py
# =====================================================================

# PASO 1 · Importar las herramientas
from pathlib import Path   # para armar la ruta del archivo del modelo
import joblib              # para cargar el modelo guardado

# PASO 2 · Cargar el modelo UNA sola vez
# Esto se ejecuta cuando arranca la API (cuando rutas/prediccion.py hace
# "from prediccion import ..."). Si lo cargáramos en cada request,
# cada respuesta tardaría mucho más.
# Path(__file__).parent = la carpeta donde está este archivo (backend).
RUTA_MODELO = Path(__file__).parent / "modelos" / "modelo_iris.joblib"
modelo = joblib.load(RUTA_MODELO)

# PASO 3 · La "traducción" de número a nombre
# El modelo responde 0, 1 o 2. La posición en esta lista nos da el nombre.
ESPECIES = ["setosa", "versicolor", "virginica"]


# PASO 4 · La función que predice
# Recibe las 4 medidas (parámetros) y devuelve un diccionario (valor de retorno).
def predecir_especie(largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo):
    # 4.1 · scikit-learn siempre espera una TABLA (lista de filas), aunque sea una sola flor.
    #       Por eso los dobles corchetes: una lista con una fila de 4 valores.
    flor = [[largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo]]

    # 4.2 · predict devuelve una lista con una predicción por fila.
    #       [0] toma la primera (y única); int() la convierte en un entero común de Python.
    numero = int(modelo.predict(flor)[0])

    # 4.3 · predict_proba devuelve qué tan seguro está el modelo de cada especie.
    #       Por ejemplo: [0.981, 0.019, 0.0]
    probabilidades = modelo.predict_proba(flor)[0]

    # 4.4 · Devolver el resultado como diccionario: FastAPI lo va a convertir en JSON
    return {
        "especie": ESPECIES[numero],
        # zip empareja cada especie con su probabilidad; round la redondea a 3 decimales.
        # float() convierte el número de numpy en uno común de Python (JSON no entiende los de numpy).
        "probabilidades": {
            especie: round(float(p), 3) for especie, p in zip(ESPECIES, probabilidades)
        },
    }


# PASO 5 · Prueba rápida (opcional): descomentar para probar el modelo sin la API
# if __name__ == "__main__":
#     print(predecir_especie(5.1, 3.5, 1.4, 0.2))
