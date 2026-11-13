# LÓGICA DEL MODELO (cumple el mismo papel que appV2.py para los nombres)
# No sabe nada de HTTP: solo carga el modelo y predice.

from pathlib import Path
import joblib

# El modelo se carga UNA sola vez, cuando arranca la API
# (cargarlo en cada request sería muy lento).
RUTA_MODELO = Path(__file__).parent / "modelos" / "modelo_iris.joblib"
modelo = joblib.load(RUTA_MODELO)

# El modelo predice un número (0, 1 o 2); esta lista lo traduce a la especie
ESPECIES = ["setosa", "versicolor", "virginica"]


def predecir_especie(largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo):
    # scikit-learn espera una lista de filas: [[...4 medidas...]]
    flor = [[largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo]]

    numero = int(modelo.predict(flor)[0])
    probabilidades = modelo.predict_proba(flor)[0]

    return {
        "especie": ESPECIES[numero],
        "probabilidades": {
            especie: round(float(p), 3) for especie, p in zip(ESPECIES, probabilidades)
        },
    }


# if __name__ == "__main__":
#     print(predecir_especie(5.1, 3.5, 1.4, 0.2))
