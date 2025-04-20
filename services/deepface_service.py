# services/deepface_service.py

import os
import cv2
import numpy as np
from PIL import Image
from deepface import DeepFace
from utils.helpers import save_temp_image, list_face_images, extract_name_from_path

DATA_DIR = "data/faces/"

def analyze_face(image_file):
    try:
        img = Image.open(image_file)
        img_array = np.array(img)

        analysis = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)
        return analysis[0]
    except Exception as e:
        return {"error": str(e)}

def verify_face_with_db(image_file):
    try:
        # Sauvegarder l’image temporairement
        temp_path = save_temp_image(image_file)

        # Parcourir la base de visages
        for face_path in list_face_images(DATA_DIR):
            result = DeepFace.verify(img1_path=temp_path, img2_path=face_path, enforce_detection=False)

            if result["verified"]:
                name = extract_name_from_path(face_path)
                return {"verified": True, "identity": name}

        return {"verified": False}

    except Exception as e:
        return {"verified": False, "error": str(e)}

def recognize_face(image_path):
    try:
        result = DeepFace.find(img_path=image_path, db_path=DATA_DIR, enforce_detection=False)
        if len(result) > 0 and len(result[0]) > 0:
            matched_path = result[0].iloc[0]["identity"]
            return extract_name_from_path(matched_path)
        return None
    except Exception as e:
        print("Erreur dans recognize_face:", e)
        return None
