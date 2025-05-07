# config/settings.py
"""
Fichier de configuration global pour FaceLogin.
Centralise les paramètres modifiables sans toucher au code métier.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "faces"
TEMP_DIR = BASE_DIR / "data" / "temp"
LOG_CSV = BASE_DIR / "database" / "presence_log.csv"

# DeepFace parameters
MODEL_NAME = "Facenet512"
DISTANCE_METRIC = "cosine"
THRESHOLD = 0.55  # Valeur max acceptable pour la distance

# Camera parameters
USB_CAMERA_INDEX = 0  # Index de la caméra USB locale
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
