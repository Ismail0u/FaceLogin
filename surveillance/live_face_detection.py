import cv2
from retinaface import RetinaFace
import numpy as np

def run_face_detection(source=0):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("❌ Impossible d'accéder à la caméra.")
        return

    print("🎥 Appuyez sur Q pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir en format compatible RetinaFace
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = RetinaFace.detect_faces(rgb)

        if isinstance(detections, dict):
            for _, face in detections.items():
                x1, y1, x2, y2 = face['facial_area']
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("🎯 Visages détectés (appuyez sur Q pour quitter)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_face_detection()
