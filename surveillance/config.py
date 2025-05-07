# surveillance/config.py

# Caméra à utiliser (0 = webcam intégrée)
CAMERA_INDEX = 0

# Seuil de reconnaissance DeepFace (distance)
RECOGNITION_THRESHOLD = 0.55

# Délai en secondes entre deux détections du même visage (anti-spam)
DUPLICATE_TIMEOUT = 60

# Répertoire de sauvegarde pour logs ou captures
LOG_DIR = "data/logs/"
