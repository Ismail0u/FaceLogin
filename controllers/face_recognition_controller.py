# controllers/face_recognition_controller.py

from services.deepface_service import verify_face_with_db, verify_group
from services.db_service import log_presence
from utils.helpers import save_temp_image, clear_temp_images

def handle_single_recognition(image_file):
    """
    Reconnaissance d’un visage unique :
    - sauvegarde temporaire
    - vérification en DB
    - log présence si identifié
    - cleanup
    """
    temp_path = None
    try:
        temp_path = save_temp_image(image_file)
        result = verify_face_with_db(temp_path)

        if result.get("verified"):
            name = result["identity"]
            log_presence(name)
            return f"✅ Bienvenue, {name} !", name
        else:
            return "❌ Visage non reconnu !", None

    except Exception as e:
        print("Erreur dans handle_single_recognition :", e)
        return f"⚠️ Erreur pendant la reconnaissance : {e}", None

    finally:
        clear_temp_images()


def handle_group_recognition(image_file):
    """
    Reconnaissance de groupe :
    - sauvegarde temporaire
    - détection multi-visages
    - log présence pour chacun
    - cleanup
    """
    temp_path = None
    try:
        temp_path = save_temp_image(image_file)
        detections = verify_group(temp_path)

        if not detections:
            return "❌ Aucun visage détecté ou reconnu.", []

        names = []
        for face in detections:
            if face["name"] != "Inconnu":
                log_presence(face["name"])
                names.append(face["name"])

        msg = "✅ " + ", ".join(names) + " reconnus !" if names else "❌ Aucun des visages détectés n’est connu."
        return msg, names

    except Exception as e:
        print("Erreur dans handle_group_recognition :", e)
        return f"⚠️ Erreur pendant la reconnaissance de groupe : {e}", []

    finally:
        clear_temp_images()
