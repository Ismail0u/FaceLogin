# surveillance/camera_monitor.py

import cv2
import os
import time
from deepface import DeepFace
from retinaface import RetinaFace
from surveillance.face_tracker import FaceTracker
from surveillance.config import CAMERA_INDEX, RECOGNITION_THRESHOLD
from utils.helpers import extract_name_from_path
from services.db_service import log_presence

DATA_DIR = "data/faces/"
MODEL_NAME = "Facenet512"
DISTANCE_METRIC = "cosine"

tracker = FaceTracker(timeout=60)  # Empêche la répétition toutes les X secondes

def recognize_and_log(face_crop):
    try:
        # Sauvegarde temporaire
        temp_file = "frame_temp.jpg"
        cv2.imwrite(temp_file, face_crop)

        # Recherche dans la base
        result = DeepFace.find(
            img_path=temp_file,
            db_path=DATA_DIR,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )

        if result and len(result[0]) > 0:
            best = result[0].iloc[0]
            cand_path = best['identity']
            distance = best['Facenet512_cosine']

            if distance <= RECOGNITION_THRESHOLD:
                name = extract_name_from_path(cand_path)

                if not tracker.is_duplicate(name):
                    print(f"✅ {name} reconnu (distance={distance:.2f}) - présence enregistrée")
                    log_presence(name)
                else:
                    print(f"⏳ {name} déjà vu récemment")
            else:
                print("❌ Distance trop élevée")
        else:
            print("❌ Aucun match trouvé")

        os.remove(temp_file)

    except Exception as e:
        print("Erreur lors de la reconnaissance :", e)

def run_surveillance():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Impossible d'accéder à la caméra.")
        return

    print("🎥 Surveillance active... Appuyez sur Q pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # RetinaFace : détection des visages
        try:
            faces = RetinaFace.detect_faces(frame)
            if faces:
                for fid, info in faces.items():
                    x1, y1, x2, y2 = info["facial_area"]
                    face_crop = frame[y1:y2, x1:x2]

                    # Dessin
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Reconnaissance
                    recognize_and_log(face_crop)

        except Exception as e:
            print("Erreur RetinaFace :", e)

        cv2.imshow("🎯 Surveillance (Q pour quitter)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_surveillance()
