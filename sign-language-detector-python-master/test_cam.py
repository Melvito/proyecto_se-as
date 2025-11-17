import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ No se pudo acceder a la cámara")
else:
    print("✅ Cámara detectada correctamente")
    cap.release()
