from services.db_service import get_all_presences
from services.email_service import send_email
from services.report_service import generate_presence_report, generate_pdf_report

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

def show_dashboard():
    st.title("📊 Dashboard des présences")
    st.markdown("Suivi des utilisateurs reconnus par reconnaissance faciale.")

    data = get_all_presences()
    if not data:
        st.info("Aucune présence enregistrée pour l’instant.")
        return

    df = pd.DataFrame(data)

    with st.expander("🔍 Filtres avancés"):
        cols = st.columns(3)

        noms = ["Tous"] + sorted(df["Nom"].unique().tolist())
        selected_nom = cols[0].selectbox("👤 Nom", noms)

        dates = ["Toutes"] + sorted(df["Date"].unique().tolist(), reverse=True)
        selected_date = cols[1].selectbox("📅 Date", dates)

        search = cols[2].text_input("🔎 Recherche (partielle)", "")

    # ✅ Application des filtres
    filtered_df = df.copy()
    if selected_nom != "Tous":
        filtered_df = filtered_df[filtered_df["Nom"] == selected_nom]
    if selected_date != "Toutes":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]
    if search:
        filtered_df = filtered_df[filtered_df["Nom"].str.contains(search, case=False)]

    # 📊 Statistiques
    col1, col2 = st.columns(2)
    col1.metric("👥 Présences affichées", len(filtered_df))
    col2.metric("👤 Utilisateurs uniques", df["Nom"].nunique())

    # 🗂️ Onglets de contenu
    tabs = st.tabs(["📋 Tableau", "📈 Graphique", "🧾 Export & Rapport"])

    # 📋 Tab 1 : Tableau
    with tabs[0]:
        st.dataframe(
            filtered_df.sort_values(by=["Date", "Heure"], ascending=False),
            use_container_width=True
        )

    # 📈 Tab 2 : Graphique
    with tabs[1]:
        graph_df = (
            filtered_df.groupby("Date")
            .size()
            .reset_index(name="Présences")
            .sort_values(by="Date")
        )

        if not graph_df.empty:
            fig = px.bar(
                graph_df, x="Date", y="Présences", text_auto=True,
                labels={"Date": "Date", "Présences": "Nombre de présences"},
                title="📅 Fréquentation par jour"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée disponible pour le graphique.")

    # 🧾 Tab 3 : Export / Rapport
    with tabs[2]:
        st.subheader("⬇️ Export")
        col_csv, col_pdf = st.columns(2)

        # Export CSV
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        col_csv.download_button(
            "📄 Télécharger CSV",
            data=csv_data,
            file_name="presences.csv",
            mime="text/csv"
        )

        # Génération PDF
        if col_pdf.button("🧾 Générer le rapport PDF"):
            pdf_bytes = generate_pdf_report(filtered_df)
            st.download_button(
                label="📥 Télécharger PDF",
                data=pdf_bytes,
                file_name=f"rapport_presences_{datetime.today().date()}.pdf",
                mime="application/pdf"
            )

        # Email
        st.markdown("---")
        if st.toggle("📤 Envoyer par email", value=False):
            with st.spinner("📬 Envoi du rapport..."):
                html = generate_presence_report()
                send_email("tonadresse@gmail.com", "📊 Rapport quotidien - FaceLogin", html)
                st.success("✅ Rapport envoyé avec succès !")
