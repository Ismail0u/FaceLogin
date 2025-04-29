import streamlit as st
from services.user_service import get_user_by_email

def login():
    st.title("🔐 Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        user = get_user_by_email(email)
        if user and user.password == password:
            st.success("✅ Connexion réussie.")
            st.session_state.authenticated = True
            st.session_state.email = user.email
            st.session_state.role = user.role
            st.rerun()
        else:
            st.error("❌ Email ou mot de passe incorrect.")

def logout():
    if st.sidebar.button("🔓 Se déconnecter"):
        st.session_state.authenticated = False
        st.session_state.email = None
        st.session_state.role = None
        st.success("👋 Déconnexion réussie.")
        st.rerun()
