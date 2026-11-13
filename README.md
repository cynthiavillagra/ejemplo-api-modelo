# API de un modelo de scikit-learn con FastAPI

Un formulario (frontend) envía las 4 medidas de una flor a una API hecha con FastAPI (backend), que le pide la predicción a un modelo de Regresión Logística entrenado con el dataset Iris.

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Devuelve `{"estado": "ok"}` si la API está funcionando |
| POST | `/predecir` | Recibe `{"largo_sepalo": 5.1, "ancho_sepalo": 3.5, "largo_petalo": 1.4, "ancho_petalo": 0.2}` y devuelve la especie y las probabilidades |

## Cómo correrlo

Desde la carpeta `backend`:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Después abrir `frontend/index.html` con Live Server.
La documentación interactiva queda en http://localhost:8000/docs

Para probar solo el modelo, sin la API: `python prediccion.py`

> El modelo se entrenó con scikit-learn 1.7.2; por eso esa versión está fijada en `requirements.txt`.

## Qué leer primero

1. `backend/prediccion.py`: la lógica del modelo (Python puro)
2. `backend/rutas/prediccion.py`: el endpoint `POST /predecir` y la validación
3. `backend/main.py`: la aplicación, CORS y el enchufe de las rutas
4. `frontend/cliente.js`: el `fetch` que llama a la API
5. `frontend/script.js`: el formulario y cómo se muestra el resultado

El modelo se entrena en el repo `ejemplo-modelo-sklearn` (`entrenar.py`).

## Dos versiones del mismo código

| Rama | Para qué |
|---|---|
| `main` | El código comentado paso a paso, para estudiar |
| `clase` | El mismo código con comentarios mínimos (el que se escribe en clase) |
