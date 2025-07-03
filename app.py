# @@streamlit run --python-version 3.11
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
import streamlit_lottie as st_lottie
import requests

from auth import login, logout
from views.dashboard_page import show_dashboard
from views.recognition_page import show_recognition
from views.add_user_page import add_user
from views.admin_page import show_admin_page
from views.surveillance_page import show_surveillance

# -------------------------------
# Initialisation session
# -------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.email = None
    st.session_state.role = None

# -------------------------------
# Authentification
# -------------------------------
if not st.session_state.authenticated:
    login()
else:
    st.set_page_config(page_title="FaceLogin", layout="centered")

    def load_lottie_url(url: str):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
            else:
                st.warning("⚠️ Animation non disponible (erreur de chargement).")
                return None
        except Exception as e:
            st.error(f"❌ Erreur Lottie : {e}")
            return None

    # -------------------------------
    # Barre latérale de navigation
    # -------------------------------
    with st.sidebar:
        st.markdown(f"👋 Connecté en tant que : **{st.session_state.email}**")
        logout()
        selected = option_menu(
            menu_title="FaceLogin",
            options=["🏠 Accueil", "Reconnaissance", "Ajouter un utilisateur", "Dashboard", "Admin","surveille"],
            icons=["house", "camera", "person-plus", "bar-chart-line", "gear","camera"],
            default_index=0,
        )

    # -------------------------------
    # PAGE 1 : Accueil
    # -------------------------------
    if selected == "🏠 Accueil":
        st.title("🎉 Bienvenue sur FaceLogin")
        st.markdown("Système de reconnaissance faciale pour le suivi de présence 📸👤")
        st.markdown(f"🕒 Date et heure actuelles : **{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}**")

        lottie = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")
        if lottie:
            st_lottie.st_lottie(lottie, height=300, key="face")
        else:
            st.info("Aucune animation disponible pour l'instant.")

    # -------------------------------
    # PAGE 2 : Reconnaissance
    # -------------------------------
    elif selected == "Reconnaissance":
        show_recognition()

    # -------------------------------
    # PAGE 3 : Ajouter un utilisateur
    # -------------------------------
    elif selected == "Ajouter un utilisateur":
        add_user()

    # -------------------------------
    # PAGE 4 : Dashboard (admin uniquement)
    # -------------------------------
    elif selected == "Dashboard":
        if st.session_state.role != "admin":
            st.error("⛔ Accès restreint. Réservé aux administrateurs.")
        else:
            show_dashboard()

    # -------------------------------
    # PAGE 5 : Admin (gestion utilisateurs)
    # -------------------------------
    elif selected == "Admin":
        if st.session_state.role != "admin":
            st.error("⛔ Accès restreint. Réservé aux administrateurs.")
        else:
            show_admin_page()

    elif selected =="surveille":
        show_surveillance()