// =====================================================================
// script.js · EL COMPORTAMIENTO DE LA PÁGINA
// ---------------------------------------------------------------------
// Qué hace: cuando se envía el formulario, lee las 4 medidas, le pide
// la predicción a la API y muestra el resultado en la página.
// Para hablar con la API usa predecirEspecie(), que está en cliente.js
// =====================================================================

// PASO 1 · Buscar en la página los elementos que vamos a usar
// querySelector busca por selector CSS: "#flor-form" = el elemento con id="flor-form"
const formulario = document.querySelector("#flor-form");
const resultado = document.querySelector("#resultado");

// PASO 2 · Decir qué hacer cuando se envía el formulario (clic en "Predecir" o Enter)
formulario.addEventListener("submit", async (evento) => {
  // 2.1 · Evitar que el navegador recargue la página (es lo que hace un formulario por defecto)
  evento.preventDefault();

  // 2.2 · Leer las 4 medidas y convertirlas a número
  // .value siempre devuelve TEXTO ("5.1"); Number() lo convierte en el número 5.1.
  // Los nombres de las claves tienen que ser IGUALES a los de la clase Flor del backend.
  const flor = {
    largo_sepalo: Number(document.querySelector("#largo_sepalo").value),
    ancho_sepalo: Number(document.querySelector("#ancho_sepalo").value),
    largo_petalo: Number(document.querySelector("#largo_petalo").value),
    ancho_petalo: Number(document.querySelector("#ancho_petalo").value)
  };

  // 2.3 · Avisar que estamos esperando la respuesta
  resultado.textContent = "Consultando al modelo...";

  // 2.4 · Intentar pedir la predicción
  // try/catch: si algo falla adentro del "try", en vez de romperse la página se ejecuta el "catch".
  try {
    const prediccion = await predecirEspecie(flor);   // esperamos la respuesta de la API
    mostrarResultado(prediccion);                     // y la dibujamos en la página
  } catch (error) {
    console.error("Error:", error);                   // el detalle queda en la consola (F12)
    resultado.textContent = "No se pudo obtener la predicción. ¿Está corriendo uvicorn main:app?";
  }
});

// PASO 3 · Dibujar el resultado: la especie y una barra por cada probabilidad
// "prediccion" llega así: { especie: "setosa", probabilidades: { setosa: 0.981, versicolor: 0.019, virginica: 0 } }
function mostrarResultado(prediccion) {
  // 3.1 · Borrar lo que hubiera antes (el "Consultando..." o un resultado anterior)
  resultado.innerHTML = "";

  // 3.2 · Crear un párrafo con la especie y agregarlo a la página
  const titulo = document.createElement("p");
  titulo.className = "especie";                              // la clase CSS que le da estilo
  titulo.textContent = "Especie: " + prediccion.especie;
  resultado.appendChild(titulo);

  // 3.3 · Recorrer las probabilidades: una vuelta por cada especie
  // Object.entries convierte el objeto en pares [especie, probabilidad]
  for (const [especie, probabilidad] of Object.entries(prediccion.probabilidades)) {
    const porcentaje = Math.round(probabilidad * 100);       // 0.981 → 98

    // 3.4 · Crear una fila con el nombre, la barra y el valor
    // El ancho del relleno de la barra es el porcentaje.
    const fila = document.createElement("div");
    fila.className = "fila";
    fila.innerHTML = `
      <span class="nombre">${especie}</span>
      <span class="barra"><span class="relleno" style="width: ${porcentaje}%"></span></span>
      <span class="valor">${porcentaje}%</span>
    `;
    resultado.appendChild(fila);
  }
}
