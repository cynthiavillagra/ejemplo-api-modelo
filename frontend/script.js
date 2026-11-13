// LA PÁGINA: lee el formulario y muestra la predicción.
// Para hablar con la API usa predecirEspecie(), que está en cliente.js

const formulario = document.querySelector("#flor-form");
const resultado = document.querySelector("#resultado");

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  // Leer las 4 medidas y convertirlas a número
  const flor = {
    largo_sepalo: Number(document.querySelector("#largo_sepalo").value),
    ancho_sepalo: Number(document.querySelector("#ancho_sepalo").value),
    largo_petalo: Number(document.querySelector("#largo_petalo").value),
    ancho_petalo: Number(document.querySelector("#ancho_petalo").value)
  };

  resultado.textContent = "Consultando al modelo...";

  try {
    const prediccion = await predecirEspecie(flor);
    mostrarResultado(prediccion);
  } catch (error) {
    console.error("Error:", error);
    resultado.textContent = "No se pudo obtener la predicción. ¿Está corriendo uvicorn main:app?";
  }
});

// Muestra la especie y una barra por cada probabilidad
function mostrarResultado(prediccion) {
  resultado.innerHTML = "";

  const titulo = document.createElement("p");
  titulo.className = "especie";
  titulo.textContent = "Especie: " + prediccion.especie;
  resultado.appendChild(titulo);

  for (const [especie, probabilidad] of Object.entries(prediccion.probabilidades)) {
    const porcentaje = Math.round(probabilidad * 100);

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
