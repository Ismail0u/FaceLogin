import streamlit as st
from utils.helpers import save_face_image

def add_user():
    st.title("➕ Ajouter un utilisateur")
    st.markdown("Ajoutez un nouvel utilisateur à la base de données de visages.")
    st.markdown("---")

    name = st.text_input("👤 Nom complet")
    st.markdown("📷 Prenez une photo avec la webcam :")
    webcam_photo = st.camera_input("Capture via webcam")

    st.markdown("📤 Ou chargez une image depuis votre appareil :")
    file_photo = st.file_uploader("Image de visage", type=["jpg", "jpeg", "png"])

    face_image = webcam_photo or file_photo
    if name and face_image:
        if st.button("✅ Enregistrer l'utilisateur"):
            save_face_image(face_image, name)
            st.success(f"🙌 Utilisateur '{name}' ajouté avec succès !")
    else:
        st.info("Veuillez remplir tous les champs.")
