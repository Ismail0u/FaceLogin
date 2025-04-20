# controllers/face_recognition_controller.py

from services.deepface_service import verify_face_with_db
from services.db_service import log_presence
from utils.helpers import save_uploaded_image

def handle_face_recognition(image_file):
    """
    Gère la reconnaissance faciale :
    - Enregistre l'image temporairement
    - Envoie à DeepFace pour reconnaissance
    - Si reconnu : log la présence
    - Retourne un message et un nom (si trouvé)
    """
    try:
        # Enregistrement temporaire de l'image
        saved_path = save_uploaded_image(image_file)

        # Reconnaissance avec DeepFace
        name = verify_face_with_db(saved_path)

        if name:
            log_presence(name)
            return f"✅ Bienvenue, {name} !", name
        else:
            return "❌ Visage non reconnu !", None

    except Exception as e:
        print("Erreur:", e)
        return f"⚠️ Erreur pendant la reconnaissance : {e}", None
