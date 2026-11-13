// =====================================================================
// cliente.js · EL CLIENTE DE LA API
// ---------------------------------------------------------------------
// Qué hace: tiene la función que habla con la API (FastAPI).
// No sabe nada del formulario ni de la página: eso lo hace script.js.
// Así, si cambia la dirección o el formato de la API, se toca solo acá.
// =====================================================================

// PASO 1 · La dirección de nuestra API (el servidor Python que levanta uvicorn)
// Cuando publiques la API, acá va la dirección pública que te dé la plataforma.
const API_URL = "http://localhost:8000";

// PASO 2 · La función que pide una predicción: POST /predecir
// "flor" es un objeto con las 4 medidas:
// { largo_sepalo: 5.1, ancho_sepalo: 3.5, largo_petalo: 1.4, ancho_petalo: 0.2 }
// "async" permite usar "await" adentro: esperar la respuesta sin congelar la página.
async function predecirEspecie(flor) {
    // 2.1 · Hacer el pedido HTTP y esperar la respuesta
    const respuesta = await fetch(API_URL + "/predecir", {
        method: "POST",                                    // POST porque le enviamos datos
        headers: { "Content-Type": "application/json" },   // avisamos que el cuerpo viaja en JSON
        body: JSON.stringify(flor)                         // convertimos el objeto en texto JSON
    });

    // 2.2 · Revisar si salió bien
    // respuesta.ok es true cuando el código de estado es 200-299.
    // Si la API contestó 422 (datos inválidos) o 500 (error del servidor), lanzamos un error
    // para que lo atrape el "catch" de script.js.
    if (!respuesta.ok) {
        throw new Error("La API respondió con error " + respuesta.status);
    }

    // 2.3 · Leer el cuerpo de la respuesta y convertirlo de JSON a objeto
    const datos = await respuesta.json();

    // 2.4 · Devolver solo la parte que interesa
    return datos.resultado;   // { especie: "setosa", probabilidades: {...} }
}
