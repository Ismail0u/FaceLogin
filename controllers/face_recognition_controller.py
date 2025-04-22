# controllers/face_recognition_controller.py

from services.deepface_service import verify_face_with_db
from services.db_service import log_presence
from utils.helpers import save_temp_image , clear_temp_images

def handle_face_recognition(image_file):
    try:
        saved_path = save_temp_image(image_file)  # image temporaire !
        result = verify_face_with_db(saved_path)


        if result.get("verified"):
            name = result.get("identity")
            log_presence(name)
            return f"✅ Bienvenue, {name} !", name
        else:
            return "❌ Visage non reconnu !", None

    except Exception as e:
        print("Erreur:", e)
        return f"⚠️ Erreur pendant la reconnaissance : {e}", None
