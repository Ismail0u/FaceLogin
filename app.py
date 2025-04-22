# app.py
import streamlit as st
from pages.dashboard_page import show_dashboard
from pages.add_user_page import add_user
from streamlit_option_menu import option_menu
from pages.recognition_page import show_recognition

st.set_page_config(page_title="FaceLogin", layout="centered")

# Navigation via barre latérale
with st.sidebar:
    selected = option_menu(
        menu_title="FaceLogin",
        options=["Reconnaissance", "Ajouter un utilisateur", "Dashboard"],
        icons=["camera", "person-plus"],
        default_index=0,
    )

# -------------------------------
# PAGE 1 : Reconnaissance Faciale
# -------------------------------
if selected == "Reconnaissance":
    show_recognition()

# -------------------------------
# PAGE 2 : Ajout d’un Utilisateur
# -------------------------------
elif selected == "Ajouter un utilisateur":
    add_user()

# -------------------------------
# PAGE 3 : Dashboard Admin
# -------------------------------
elif selected == "Dashboard":
    show_dashboard()
