# utils/helpers.py

import os
import uuid
from PIL import Image

TEMP_DIR = "data/temp/"
FACE_DIR = "data/faces/"

# Sauvegarde une image temporaire avec un nom unique
def save_temp_image(image_file):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(TEMP_DIR, filename)

    image = Image.open(image_file)
    image.save(path)

    return path

# Liste toutes les images de visages dans le dossier de base
def list_face_images(folder=FACE_DIR):
    if not os.path.exists(folder):
        os.makedirs(folder)

    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Extrait le nom de l’utilisateur à partir du nom de fichier de l’image
def extract_name_from_path(image_path):
    filename = os.path.basename(image_path)
    name = os.path.splitext(filename)[0]
    return name.capitalize()


def save_uploaded_image(image_file):
    """
    Enregistre une image uploadée dans data/faces avec un nom unique.
    """
    folder = "data/faces/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as f:
        f.write(image_file.read())

    return file_path

def save_face_image(image_file, name, data_dir="data/faces"):
    os.makedirs(data_dir, exist_ok=True)
    ext = image_file.name.split('.')[-1]
    filename = f"{name}.{ext}"
    save_path = os.path.join(data_dir, filename)

    with open(save_path, "wb") as f:
        f.write(image_file.read())

    return save_path

