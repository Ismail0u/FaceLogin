# services/deepface_service.py
import os
import cv2
import numpy as np
import uuid
from deepface import DeepFace
from retinaface import RetinaFace
from utils.helpers import save_temp_image, extract_name_from_path, clear_temp_images

# Configuration
data_dir = "data/faces/"
MODEL_NAME = "Facenet512"
DISTANCE_METRIC = "cosine"
THRESHOLD = 0.55  # Ajustable selon les tests
TEMP_DIR = "data/temp/"


def analyze_face(image_input):
    """
    Analyse les émotions d'un visage unique.
    Accepte un chemin ou un fichier (file-like).
    """
    try:
        # Préparer l'image
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
        else:
            file_bytes = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image non valide.")
        # Analyse emotion
        analysis = DeepFace.analyze(
            img, actions=['emotion'], enforce_detection=False
        )
        return analysis[0]
    except Exception as e:
        print("❌ Erreur dans analyze_face:", e)
        return {"error": str(e)}


def verify_face_with_db(image_input):
    """
    Vérifie un visage unique contre la base.
    Retourne dict {'verified', 'identity', 'distance'}.
    """
    try:
        # Gérer chemin ou fichier
        if isinstance(image_input, str):
            temp_path = image_input
        else:
            temp_path = save_temp_image(image_input)

        # Recherche de similarités
        df_list = DeepFace.find(
            img_path=temp_path,
            db_path=data_dir,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )
        # si aucun résultat
        if not df_list or df_list[0].empty:
            return {"verified": False}

        # Sélection du meilleur match
        best = df_list[0].iloc[0]
        cand_path = best['identity']
        cand_name = extract_name_from_path(cand_path)

        # Vérification stricte
        verif = DeepFace.verify(
            img1_path=temp_path,
            img2_path=cand_path,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )
        dist = verif.get('distance', 1.0)
        ok = verif.get('verified', False)
        if ok and dist <= THRESHOLD:
            return {"verified": True, "identity": cand_name, "distance": dist}
        return {"verified": False, "distance": dist}

    except Exception as e:
        print("❌ Erreur dans verify_face_with_db:", e)
        return {"verified": False, "error": str(e)}


def recognize_face(image_path):
    """
    Recherche un visage unique via find, renvoie juste le nom ou None.
    """
    try:
        df_list = DeepFace.find(
            img_path=image_path,
            db_path=data_dir,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )
        if df_list and not df_list[0].empty:
            return extract_name_from_path(df_list[0].iloc[0]['identity'])
        return None
    except Exception as e:
        print("❌ Erreur dans recognize_face:", e)
        return None


def verify_group(image_input):
    """
    Détecte et reconnaît plusieurs visages dans une image de groupe.
    Retourne une liste de dicts {face_id, coords, name, score}.
    """
    clear_temp_images()
    try:
        # obtenir un chemin temporaire
        if isinstance(image_input, str):
            temp_path = image_input
        else:
            temp_path = save_temp_image(image_input)

        # charger l'image
        img = cv2.imread(temp_path)
        if img is None:
            return []

        # détection multi-visages
        detections = RetinaFace.detect_faces(temp_path)
        results = []
        if not detections:
            return results

        for face_id, info in detections.items():
            x1, y1, x2, y2 = info['facial_area']
            face_crop = img[y1:y2, x1:x2]
            # sauver chaque crop pour DeepFace.find
            crop_path = os.path.join(TEMP_DIR, f"crop_{uuid.uuid4().hex}.jpg")
            cv2.imwrite(crop_path, face_crop)

            # init
            name, score = "Inconnu", None
            # recherche best match
            df_list = DeepFace.find(
                img_path=crop_path,
                db_path=data_dir,
                model_name=MODEL_NAME,
                distance_metric=DISTANCE_METRIC,
                enforce_detection=False
            )
            if df_list and not df_list[0].empty:
                best = df_list[0].iloc[0]
                cand_path = best['identity']
                cand_name = extract_name_from_path(cand_path)
                verif = DeepFace.verify(
                    img1_path=crop_path,
                    img2_path=cand_path,
                    model_name=MODEL_NAME,
                    distance_metric=DISTANCE_METRIC,
                    enforce_detection=False
                )
                dist = verif.get('distance', None)
                ok = verif.get('verified', False)
                if ok and dist <= THRESHOLD:
                    name, score = cand_name, dist
            results.append({
                'face_id': face_id,
                'coords': (x1, y1, x2-x1, y2-y1),
                'name': name,
                'score': score
            })
        clear_temp_images()
        return results

    except Exception as e:
        print("❌ Erreur dans verify_group:", e)
        clear_temp_images()
        return []

