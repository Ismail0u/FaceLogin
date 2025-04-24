import streamlit as st
from services.user_service import get_all_users, add_user, update_user, delete_user
from services.db_service import get_all_presences
from services.report_service import generate_pdf_report
from services.email_service import send_email
import pandas as pd

def show_admin_page():
    st.title("🧑‍💼 Vue Admin Complète")
    st.markdown("Panneau de contrôle pour la gestion des utilisateurs et des présences.")

    tab1, tab2, tab3 = st.tabs(["👥 Utilisateurs", "📅 Présences", "📊 Statistiques"])

    # -------------------- UTILISATEURS --------------------
    with tab1:
        st.subheader("👥 Gestion des utilisateurs")
        users = get_all_users()

        # ✅ Ajout utilisateur
        with st.expander("➕ Ajouter un utilisateur"):
            with st.form("ajout_form", clear_on_submit=True):
                nom = st.text_input("Nom complet")
                email = st.text_input("Adresse email")
                role = st.selectbox("Rôle", ["utilisateur", "admin", "manager"])
                submitted = st.form_submit_button("Ajouter")
                if submitted:
                    if nom and email:
                        add_user(nom, email, role)
                        st.success(f"✅ Utilisateur {nom} ajouté avec succès.")
                        st.experimental_rerun()
                    else:
                        st.error("❌ Tous les champs sont requis.")

        # 📋 Liste des utilisateurs
        st.subheader("📋 Liste des utilisateurs")
        for user in users:
            with st.expander(f"👤 {user.nom} ({user.role})"):
                col1, col2 = st.columns(2)

                # ✏️ Modification
                with col1.form(f"update_form_{user.id}"):
                    new_nom = st.text_input("Nom", user.nom)
                    new_email = st.text_input("Email", user.email)
                    new_role = st.selectbox("Rôle", ["utilisateur", "admin", "manager"],
                                            index=["utilisateur", "admin", "manager"].index(user.role))
                    update_btn = st.form_submit_button("💾 Enregistrer")
                    if update_btn:
                        update_user(user.id, new_nom, new_email, new_role)
                        st.success("✅ Utilisateur mis à jour.")
                        st.experimental_rerun()

                # ❌ Suppression
                with col2:
                    if st.button("🗑️ Supprimer", key=f"delete_{user.id}"):
                        delete_user(user.id)
                        st.warning(f"❌ Utilisateur {user.nom} supprimé.")
                        st.experimental_rerun()

    # -------------------- PRÉSENCES --------------------
    with tab2:
        st.subheader("📅 Liste complète des présences")
        data = get_all_presences()
        if not data:
            st.info("Aucune présence enregistrée.")
        else:
            df = pd.DataFrame(data)
            st.dataframe(df.sort_values(by=["Date", "Heure"], ascending=False), use_container_width=True)

            col1, col2 = st.columns(2)

            # 🧾 Génération PDF
            if col1.button("📄 Générer PDF global"):
                pdf = generate_pdf_report(df)
                st.download_button(
                    "📥 Télécharger PDF",
                    data=pdf,
                    file_name="rapport_global_presences.pdf",
                    mime="application/pdf"
                )

            # 📤 Envoi Email
            if col2.button("📧 Envoyer par email"):
                html_content = df.to_html(index=False)
                send_email("tonemail@exemple.com", "📊 Rapport des présences", html_content)
                st.success("✅ Rapport envoyé avec succès.")

    # -------------------- STATISTIQUES --------------------
    with tab3:
        st.subheader("📊 Statistiques globales")
        if not data:
            st.warning("Aucune donnée disponible.")
        else:
            df = pd.DataFrame(data)

            col1, col2, col3 = st.columns(3)
            col1.metric("👥 Total Présences", len(df))
            col2.metric("📆 Jours distincts", df["Date"].nunique())
            col3.metric("🧑‍🤝‍🧑 Utilisateurs uniques", df["Nom"].nunique())

            st.markdown("### 📈 Courbe de fréquentation")
            graph_df = (
                df.groupby("Date")
                .size()
                .reset_index(name="Présences")
                .sort_values("Date")
            )

            if not graph_df.empty:
                fig = px.line(
                    graph_df, x="Date", y="Présences",
                    title="Présences par jour",
                    markers=True,
                    labels={"Date": "Date", "Présences": "Nombre de présences"}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pas encore assez de données.")

