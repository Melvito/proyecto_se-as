from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
from io import BytesIO
import base64

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# 🔹 Cargar modelo entrenado
model_dict = pickle.load(open('../model.p', 'rb'))
model = model_dict['model']

# 🔹 Configurar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recibir la imagen desde el frontend
        data = request.get_json()
        image_data = data['image']
        print("📩 Imagen recibida")

        # 🔹 Decodificar la imagen Base64
        image_data = image_data.split(',')[1]
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        print("✅ Imagen decodificada correctamente")

        # 🔹 Procesar con MediaPipe
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        print("🔍 Procesando con MediaPipe...")

        data_aux = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x_ = [lm.x for lm in hand_landmarks.landmark]
                y_ = [lm.y for lm in hand_landmarks.landmark]

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

            # 🔹 Hacer la predicción
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]
            print("🧠 Predicción:", predicted_character)
        else:
            predicted_character = "No detectado"
            print("⚠️ No se detectó ninguna mano")

        return jsonify({'prediccion': predicted_character})

    except Exception as e:
        print("💥 Error en el servidor:", e)
        return jsonify({'prediccion': 'Error interno', 'detalle': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Servidor Flask corriendo en http://127.0.0.1:5000")
    app.run(debug=True)

