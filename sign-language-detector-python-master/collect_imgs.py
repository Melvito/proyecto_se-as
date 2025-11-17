import os
import cv2

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 🔤 Primeras 5 letras del abecedario
classes = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'Ñ']
dataset_size = 100  # puedes subirlo a 200 si quieres mejor precisión

# Usa el driver correcto para Windows (índice 0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ No se pudo acceder a la cámara. Intenta cambiar el índice a 1.")
    exit()

for label in classes:
    class_dir = os.path.join(DATA_DIR, label)
    os.makedirs(class_dir, exist_ok=True)

    print(f'📸 Recolectando datos para la letra "{label}"')
    print('Presiona "Q" cuando estés lista para empezar.')

    # Esperar hasta que el usuario presione Q
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ No se pudo leer frame de la cámara.")
            continue
        cv2.putText(frame, f'Letra: {label} - Presiona "Q" para iniciar', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    counter = 0
    print("Grabando imágenes... Presiona ESC para salir antes.")
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ No se pudo leer frame, intentando de nuevo...")
            continue
        cv2.imshow('frame', frame)
        key = cv2.waitKey(25) & 0xFF
        if key == 27:  # ESC
            break
        cv2.imwrite(os.path.join(class_dir, f'{counter}.jpg'), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()

print("✅ Captura completada.")
