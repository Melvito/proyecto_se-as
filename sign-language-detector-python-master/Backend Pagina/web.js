const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultado = document.getElementById("resultado");
const boton = document.getElementById("capture");
const ctx = canvas.getContext("2d");

// Activar cámara
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Error al acceder a la cámara:", err);
  });

// Capturar imagen y enviar al backend
boton.addEventListener("click", async () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imageData = canvas.toDataURL("image/jpeg");

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData })
    });

    const data = await response.json();
    resultado.textContent = `Resultado: ${data.prediccion}`;
  } catch (error) {
    console.error("Error al predecir:", error);
    resultado.textContent = "❌ Error al conectar con el servidor.";
  }
});
