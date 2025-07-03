# pages/surveillance_page.py
import cv2
import time
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from services.deepface_service import verify_group, MODEL_NAME, DISTANCE_METRIC, THRESHOLD

st.set_page_config(page_title="🎥 Surveillance Live", layout="wide")

def show_surveillance():
    st.title("🎥 Surveillance Live")
    st.markdown(
        """
        - Sélectionnez votre source (0=webcam locale, ou URL RTSP/HTTP).
        - Cochez “Reconnaissance” pour tenter d’identifier les visages.
        """
    )
    source = st.sidebar.text_input("Source vidéo", value="0")
    do_recognize = st.sidebar.checkbox("🔍 Reconnaissance", value=False)
    fps_limit = st.sidebar.slider("FPS max", 1, 30, 5)

    placeholder = st.empty()
    last_time = 0.0

    # Ouvrir le flux
    try:
        src = int(source) if source.isdigit() else source
        cap = cv2.VideoCapture(src)
        if not cap.isOpened():
            st.error("❌ Impossible d'ouvrir la source vidéo.")
            return
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation de la caméra : {e}")
        return

    st.sidebar.success("Flux vidéo démarré ✅")
    stop = st.sidebar.button("🛑 Arrêter")

    while cap.isOpened() and not stop:
        # Limiter le FPS
        if time.time() - last_time < 1.0 / fps_limit:
            continue
        last_time = time.time()

        ret, frame = cap.read()
        if not ret:
            st.warning("📡 Plus de flux.")
            break

        # Détecter (uniquement) les boîtes
        faces = {}
        try:
            # RetinaFace attend un path ou array RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = verify_group(rgb) if do_recognize else [
                {**info, 'name': '', 'score': None}
                for _, info in __import__('retinaface').RetinaFace.detect_faces(rgb).items()
            ]
        except Exception:
            # fallback détection par RetinaFace directement
            det = __import__('retinaface').RetinaFace.detect_faces(rgb) or {}
            faces = [
                {'face_id': fid,
                 'coords': (info['facial_area'][0],
                            info['facial_area'][1],
                            info['facial_area'][2] - info['facial_area'][0],
                            info['facial_area'][3] - info['facial_area'][1]),
                 'name': '', 'score': None}
                for fid, info in det.items()
            ]

        # Annoter
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        for r in faces:
            x, y, w, h = r['coords']
            draw.rectangle([x, y, x+w, y+h], outline="lime", width=2)
            if do_recognize and r.get('name'):
                label = f"{r['name']} ({r['score']:.2f})"
                draw.text((x, max(y-12, 0)), label, fill="lime")

        # Affichage
        placeholder.image(pil_img, use_column_width=True)

    cap.release()
    placeholder.empty()
    st.sidebar.info("🔌 Flux arrêté.")

# Entry point
if __name__ == "__main__":
    show_surveillance()
