from services.db_service import get_all_presences
from services.email_service import send_email
from services.report_service import generate_presence_report, generate_pdf_report

import pandas as pd
import plotly.express as px
import streamlit as st

def show_dashboard():
    st.title("📊 Dashboard des présences")
    st.markdown("Suivi des utilisateurs reconnus par reconnaissance faciale.")

    data = get_all_presences()
    if not data:
        st.info("Aucune présence enregistrée pour l’instant.")
        return

    df = pd.DataFrame(data)

    # 🔍 Filtres dynamiques
    with st.expander("🔍 Filtres avancés"):
        col1, col2, col3 = st.columns(3)

        noms = ["Tous"] + sorted(df["Nom"].unique())
        selected_nom = col1.selectbox("👤 Nom", noms)

        dates = ["Toutes"] + sorted(df["Date"].unique(), reverse=True)
        selected_date = col2.selectbox("📅 Date", dates)

        search_query = col3.text_input("🔎 Recherche partielle")

    # ✅ Application des filtres
    filtered_df = df.copy()
    if selected_nom != "Tous":
        filtered_df = filtered_df[filtered_df["Nom"] == selected_nom]
    if selected_date != "Toutes":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]
    if search_query:
        filtered_df = filtered_df[filtered_df["Nom"].str.contains(search_query, case=False)]

    # 📊 Statistiques
    st.markdown("### 📈 Statistiques")
    stat1, stat2 = st.columns(2)
    stat1.metric("👥 Présences affichées", len(filtered_df))
    stat2.metric("👤 Utilisateurs uniques", df["Nom"].nunique())

    # 🗂️ Onglets de contenu
    tab1, tab2, tab3 = st.tabs(["📋 Tableau", "📈 Graphique", "🧾 Export & Rapport"])

    with tab1:
        st.markdown("### 📋 Tableau des présences")
        st.dataframe(
            filtered_df.sort_values(by=["Date", "Heure"], ascending=False),
            use_container_width=True
        )

    with tab2:
        st.markdown("### 📈 Fréquentation par jour")
        graph_df = (
            filtered_df.groupby("Date")
            .size()
            .reset_index(name="Présences")
            .sort_values("Date")
        )
        if not graph_df.empty:
            fig = px.line(
                graph_df, x="Date", y="Présences",
                markers=True,
                title="Courbe des présences par jour",
                labels={"Date": "Date", "Présences": "Nombre de présences"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée à afficher pour le graphique.")

    with tab3:
        st.markdown("### 📄 Export et rapport")
        export_col1, export_col2 = st.columns(2)

        # ⬇️ Export CSV
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        export_col1.download_button(
            label="📥 Télécharger CSV",
            data=csv_data,
            file_name="presences_filtrées.csv",
            mime="text/csv"
        )

        # 🧾 Génération du PDF
        if export_col2.button("🧾 Générer le rapport PDF"):
            pdf_bytes = generate_pdf_report(filtered_df)
            st.download_button(
                label="📄 Télécharger PDF",
                data=pdf_bytes,
                file_name="rapport_presences.pdf",
                mime="application/pdf"
            )

        # 📤 Email
        st.markdown("---")
        if st.toggle("📬 Envoyer le rapport du jour par email"):
            with st.spinner("Envoi en cours..."):
                html_report = generate_presence_report()
                send_email("tonadresse@gmail.com", "📊 Rapport quotidien - FaceLogin", html_report)
                st.success("✅ Rapport envoyé avec succès.")
