
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultado = document.getElementById("resultado");
const ctx = canvas.getContext("2d");

// Activar cámara automáticamente
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; })
  .catch(err => console.error("Error al acceder a la cámara:", err));

// Enviar imagen automáticamente cada 1 segundo
setInterval(() => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL("image/jpeg");

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imageData })
  })
  .then(res => res.json())
  .then(data => {
    resultado.textContent = `Resultado: ${data.prediccion}`;
  })
  .catch(() => {
    resultado.textContent = "Error conectando al servidor";
  });

}, 1000);
