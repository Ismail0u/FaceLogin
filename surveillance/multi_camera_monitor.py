# surveillance/multi_camera_monitor.py

import threading
from surveillance.camera_monitor import run_surveillance
from surveillance.config import CAMERA_INDEXES

def start_camera(index):
    print(f"🎥 Démarrage de la caméra {index}")
    run_surveillance(index)

def run_multi_camera():
    threads = []
    for idx in CAMERA_INDEXES:
        t = threading.Thread(target=start_camera, args=(idx,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    run_multi_camera()
