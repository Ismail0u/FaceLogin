import streamlit as st
import pandas as pd
import plotly.express as px
from services.user_service import get_all_users, add_user, update_user, delete_user
from services.db_service import get_all_presences
from services.report_service import generate_pdf_report
from services.email_service import send_email

def show_admin_page():
    st.title("🧑‍💼 Vue Admin Complète")
    st.markdown("Panneau de contrôle pour la gestion des utilisateurs et des présences.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["👥 Utilisateurs", "📅 Présences", "📊 Statistiques"])

    # -------------------- TAB 1 : UTILISATEURS --------------------
    with tab1:
        st.subheader("👥 Gestion des utilisateurs")
        users = get_all_users()

        # ➕ Formulaire d'ajout
        with st.expander("➕ Ajouter un utilisateur"):
            with st.form("form_add_user", clear_on_submit=True):
                nom = st.text_input("Nom complet")
                email = st.text_input("Adresse email")
                role = st.selectbox("Rôle", ["utilisateur", "admin", "manager"])
                if st.form_submit_button("Ajouter"):
                    if nom and email:
                        add_user(nom, email, role)
                        st.success(f"✅ Utilisateur {nom} ajouté.")
                        st.rerun()
                    else:
                        st.error("❌ Tous les champs sont requis.")

        # 📋 Liste des utilisateurs
        for user in users:
            with st.expander(f"👤 {user.nom} ({user.role})"):
                col1, col2 = st.columns(2)

                # ✏️ Edition
                with col1.form(f"update_form_{user.id}"):
                    new_nom = st.text_input("Nom", value=user.nom)
                    new_email = st.text_input("Email", value=user.email)
                    new_role = st.selectbox("Rôle", ["utilisateur", "admin", "manager"], index=["utilisateur", "admin", "manager"].index(user.role))
                    if st.form_submit_button("💾 Enregistrer"):
                        update_user(user.id, new_nom, new_email, new_role)
                        st.success("✅ Utilisateur mis à jour.")
                        st.rerun()

                # ❌ Suppression
                if col2.button("🗑️ Supprimer", key=f"delete_{user.id}"):
                    delete_user(user.id)
                    st.warning(f"❌ Utilisateur {user.nom} supprimé.")
                    st.rerun()

    # -------------------- TAB 2 : PRÉSENCES --------------------
    with tab2:
        st.subheader("📅 Présences enregistrées")
        data = get_all_presences()

        if not data:
            st.info("Aucune présence trouvée.")
        else:
            df = pd.DataFrame(data)
            st.dataframe(df.sort_values(by=["Date", "Heure"], ascending=False), use_container_width=True)

            col1, col2 = st.columns(2)

            if col1.button("📄 Générer PDF"):
                pdf = generate_pdf_report(df)
                st.download_button("📥 Télécharger PDF", pdf, "rapport_presences.pdf", "application/pdf")

            if col2.button("📧 Envoyer par email"):
                html = df.to_html(index=False)
                send_email("tonemail@exemple.com", "📊 Rapport des présences", html)
                st.success("✅ Email envoyé.")

    # -------------------- TAB 3 : STATISTIQUES --------------------
    with tab3:
        st.subheader("📊 Statistiques globales")
        data = get_all_presences()
        if not data:
            st.info("Pas de données disponibles.")
        else:
            df = pd.DataFrame(data)
            col1, col2, col3 = st.columns(3)
            col1.metric("📋 Présences totales", len(df))
            col2.metric("📅 Jours uniques", df["Date"].nunique())
            col3.metric("👤 Utilisateurs uniques", df["Nom"].nunique())

            graph_df = (
                df.groupby("Date")
                .size()
                .reset_index(name="Présences")
                .sort_values("Date")
            )

            if not graph_df.empty:
                fig = px.line(
                    graph_df, x="Date", y="Présences",
                    title="📈 Courbe des présences par jour",
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
