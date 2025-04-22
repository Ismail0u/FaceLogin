# services/deepface_service.py

import os
import cv2
import numpy as np
from deepface import DeepFace
from utils.helpers import save_temp_image, extract_name_from_path

DATA_DIR = "data/faces/"
MODEL_NAME = "Facenet512"
DISTANCE_METRIC = "cosine"
THRESHOLD = 0.55  # Ajustable selon les tests


def analyze_face(image_input):
    """
    Analyse les émotions du visage.
    Accepte un fichier image ou un chemin.
    """
    try:
        if isinstance(image_input, str):  # Cas : chemin
            img = cv2.imread(image_input)
        else:  # Cas : fichier image (file-like object)
            file_bytes = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Image non valide ou introuvable.")

        # Analyse avec DeepFace
        analysis = DeepFace.analyze(
            img,
            actions=['emotion'],
            enforce_detection=False
        )
        return analysis[0]
    except Exception as e:
        print("❌ Erreur dans analyze_face:", e)
        return {"error": str(e)}


def verify_face_with_db(image_input):
    """
    Compare une image (chemin ou fichier) avec la base d’images.
    Renvoie l’identité si un match fiable est trouvé.
    """
    try:
        # 1. Gérer le cas chemin ou fichier
        if isinstance(image_input, str):
            temp_path = image_input
        else:
            temp_path = save_temp_image(image_input)

        # 2. Recherche dans la base
        results = DeepFace.find(
            img_path=temp_path,
            db_path=DATA_DIR,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )

        if not results or len(results[0]) == 0:
            print("❌ Aucun visage similaire trouvé dans la base.")
            return {"verified": False}

        # 3. Meilleur match
        best_match = results[0].iloc[0]
        best_match_path = best_match["identity"]
        identity_name = extract_name_from_path(best_match_path)

        # 4. Vérification stricte
        verification = DeepFace.verify(
            img1_path=temp_path,
            img2_path=best_match_path,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )

        distance = verification.get("distance", 1.0)
        verified = verification.get("verified", False)

        print(f"🔍 Match : {identity_name} | Distance = {distance:.4f} | Verified = {verified}")

        if verified and distance <= THRESHOLD:
            return {"verified": True, "identity": identity_name, "distance": distance}
        else:
            return {"verified": False, "distance": distance}

    except Exception as e:
        print("❌ Erreur dans verify_face_with_db:", e)
        return {"verified": False, "error": str(e)}


def recognize_face(image_path):
    """
    Trouve un match dans la base à partir d’un chemin d’image.
    Retourne le nom si trouvé, sinon None.
    """
    try:
        results = DeepFace.find(
            img_path=image_path,
            db_path=DATA_DIR,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False
        )

        if len(results) > 0 and len(results[0]) > 0:
            matched_path = results[0].iloc[0]["identity"]
            return extract_name_from_path(matched_path)

        return None
    except Exception as e:
        print("❌ Erreur dans recognize_face:", e)
        return None
