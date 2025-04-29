# utils/helpers.py

import os
import uuid
import numpy as np
import cv2
from PIL import Image

TEMP_DIR = "data/temp/"
FACE_DIR = "data/faces/"

# 🔹 Rewind & lire les données brutes d'un fichier uploadé
def _read_image_bytes(image_file):
    image_file.seek(0)
    return np.asarray(bytearray(image_file.read()), dtype=np.uint8)

# 🔹 Sauvegarde une image temporaire (pour la reconnaissance)
def save_temp_image(image_file):
    os.makedirs(TEMP_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(TEMP_DIR, filename)

    buf = _read_image_bytes(image_file)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Impossible de décoder l'image temporaire.")
    cv2.imwrite(path, image)
    return path

# 🔹 Liste les fichiers d'images dans le dossier des visages
def list_face_images(folder=FACE_DIR):
    os.makedirs(folder, exist_ok=True)
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

# 🔹 Extrait un nom à partir du nom de fichier
def extract_name_from_path(image_path):
    filename = os.path.basename(image_path)
    name = os.path.splitext(filename)[0]
    return name.replace("_", " ").capitalize()

# 🔹 Enregistre une image uploadée (dans faces) avec OpenCV
def save_uploaded_image(image_file, folder=FACE_DIR):
    os.makedirs(folder, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(folder, filename)

    buf = _read_image_bytes(image_file)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Impossible de décoder l'image uploadée.")
    cv2.imwrite(file_path, image)
    return file_path

# 🔹 Enregistre une image avec un nom spécifique (OpenCV)
def save_face_image(image_file, name, data_dir=FACE_DIR):
    os.makedirs(data_dir, exist_ok=True)
    ext = image_file.name.split('.')[-1].lower()
    filename = f"{name}.{ext}"
    save_path = os.path.join(data_dir, filename)

    buf = _read_image_bytes(image_file)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Impossible de décoder l'image pour l'utilisateur.")
    cv2.imwrite(save_path, image)
    return save_path

# 🔹 Supprimer tous les fichiers temporaires
def clear_temp_images():
    if os.path.exists(TEMP_DIR):
        for f in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

