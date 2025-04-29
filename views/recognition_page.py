# pages/recognition_page.py
import streamlit as st
from services.deepface_service import verify_group
from utils.helpers import clear_temp_images
from datetime import datetime
from PIL import Image, ImageDraw

def show_recognition():
    st.title("📸 Reconnaissance de Groupe")
    st.markdown("Système de reconnaissance faciale multi-visages 📷")
    st.markdown("---")

    uploaded = st.file_uploader("🖼️ Téléversez une image de groupe", type=["jpg", "jpeg", "png"])
    if not uploaded:
        st.info("Veuillez uploader une image pour commencer.")
        return

    # Charge l'image d'origine et calcule le scale pour l'affichage
    img = Image.open(uploaded)
    orig_w, orig_h = img.size
    disp_w, disp_h = 600, 400
    scale_w, scale_h = disp_w / orig_w, disp_h / orig_h

    # Affiche la version redimensionnée
    resized = img.resize((disp_w, disp_h))
    st.image(resized, caption="Image reçue", use_container_width=False)

    if st.button("🔍 Détecter et reconnaître tous les visages"):
        with st.spinner("Analyse en cours..."):
            results = verify_group(uploaded)

        if results:
            st.markdown(f"### 🔎 {len(results)} visage(s) détecté(s) à {datetime.now().strftime('%H:%M:%S')}")

            # Prépare l'annotation
            annotated = resized.copy()
            draw = ImageDraw.Draw(annotated)

            # Colonne pour chaque crop de visage
            cols = st.columns(len(results))

            for i, face in enumerate(results):
                x, y, w, h = face['coords']
                # mise à l'échelle pour annotation sur la version redimensionnée
                x1, y1 = int(x * scale_w), int(y * scale_h)
                x2, y2 = int((x + w) * scale_w), int((y + h) * scale_h)

                # dessine rectangle et label
                draw.rectangle([(x1, y1), (x2, y2)], outline="lime", width=3)
                label = face['name'] + (f" ({face['score']:.2f})" if face['score'] is not None else "")
                draw.text((x1, max(y1 - 15, 0)), label, fill="lime")

                # extrait et affiche le crop d'origine (non redimensionné) pour conserver la qualité
                crop = img.crop((x, y, x + w, y + h))
                cols[i].image(crop.resize((100, 100)), caption=label, use_container_width=False)

            # affiche l'image annotée
            st.image(annotated, caption="Résultats annotés", use_container_width=False)
        else:
            st.warning("Aucun visage détecté ou reconnu.")

        # Nettoyage des temporaires
        clear_temp_images()
