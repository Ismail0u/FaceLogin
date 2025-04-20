import streamlit as st
from controllers.face_recognition_controller import handle_face_recognition
from utils.helpers import save_face_image
from datetime import datetime
from streamlit_option_menu import option_menu
import os
from PIL import Image

def show_recognition():
    st.title("📸 FaceLogin - Reconnaissance")
    st.subheader("Système de reconnaissance faciale de présence")
    st.markdown("---")

    uploaded_image = st.file_uploader("🖼️ Téléversez une image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Image reçue", width=300)

        if st.button("🔍 Lancer la reconnaissance"):
            with st.spinner("Analyse en cours..."):
                result_msg, recognized_name = handle_face_recognition(uploaded_image)

            st.markdown("---")
            st.success(result_msg) if recognized_name else st.error(result_msg)

            if recognized_name:
                st.markdown(f"🕒 **Heure d'enregistrement :** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

                # Afficher l'image enregistrée connue
                known_image_path_jpg = os.path.join("data", "faces", f"{recognized_name}.jpg")
                known_image_path_png = os.path.join("data", "faces", f"{recognized_name}.png")
                known_image_path_jpeg = os.path.join("data", "faces", f"{recognized_name}.jpeg")

                if os.path.exists(known_image_path_jpg):
                    path = known_image_path_jpg
                elif os.path.exists(known_image_path_png):
                    path = known_image_path_png
                elif os.path.exists(known_image_path_jpeg):
                    path = known_image_path_jpeg
                else:
                    path = None

                if path:
                    st.markdown("🧑‍🎓 **Photo enregistrée correspondante :**")
                    st.image(Image.open(path), width=300)
                else:
                    st.warning("⚠️ Aucune image enregistrée trouvée pour cette personne.")
    else:
        st.info("Veuillez uploader une image pour commencer.")
