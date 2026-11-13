// CLIENTE DE LA API: la función que habla con el modelo (FastAPI)
// (no sabe nada del formulario; eso lo hace script.js)

// Dirección de nuestra API (servidor Python)
const API_URL = "http://localhost:8000";

// Pedir una predicción: POST /predecir
// "flor" es un objeto con las 4 medidas:
// { largo_sepalo: 5.1, ancho_sepalo: 3.5, largo_petalo: 1.4, ancho_petalo: 0.2 }
async function predecirEspecie(flor) {
    const respuesta = await fetch(API_URL + "/predecir", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(flor)
    });

    if (!respuesta.ok) {
        throw new Error("La API respondió con error " + respuesta.status);
    }

    const datos = await respuesta.json();
    return datos.resultado;   // { especie: "setosa", probabilidades: {...} }
}
