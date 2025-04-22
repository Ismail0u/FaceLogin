from services.db_service import get_all_presences
import pandas as pd
import plotly.express as px
import streamlit as st

from services.email_service import send_email
from services.report_service import generate_presence_report


def show_dashboard():
    st.title("📊 Présences enregistrées")
    st.markdown("Liste des utilisateurs reconnus avec heure de passage.")
    st.markdown("---")

    data = get_all_presences()

    if data:
        df = pd.DataFrame(data)

        # 📌 Filtrage dynamique
        noms = df["Nom"].unique().tolist()
        selected_nom = st.selectbox("🔍 Filtrer par nom :", options=["Tous"] + noms)

        dates = sorted(df["Date"].unique(), reverse=True)
        selected_date = st.selectbox("📅 Filtrer par date :", options=["Toutes"] + dates)

        search = st.text_input("📝 Rechercher un nom (partiel)")

        filtered_df = df.copy()

        if selected_nom != "Tous":
            filtered_df = filtered_df[filtered_df["Nom"] == selected_nom]

        if selected_date != "Toutes":
            filtered_df = filtered_df[filtered_df["Date"] == selected_date]

        if search:
            filtered_df = filtered_df[filtered_df["Nom"].str.contains(search, case=False)]

        # 📊 Statistiques
        st.markdown(f"👥 **Présences affichées :** {len(filtered_df)} / {len(df)}")
        st.markdown(f"👤 **Présences uniques :** {df['Nom'].nunique()}")

        # 🧾 Tableau
        st.dataframe(filtered_df[["Nom", "Date", "Heure"]].sort_values(by="Date", ascending=False),
                     use_container_width=True)

        # ⬇️ Export
        csv = filtered_df[["Nom", "Date", "Heure"]].to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger (CSV filtré)", csv, "presences_filtrées.csv", "text/csv")
    else:
        st.info("Aucune présence enregistrée pour l’instant.")

    # 📈 Graphe : Présences par jour
    presences_par_jour = (
        filtered_df.groupby("Date")
        .size()
        .reset_index(name="Nombre de présences")
        .sort_values(by="Date")
    )

    if not presences_par_jour.empty:
        fig = px.bar(
            presences_par_jour,
            x="Date",
            y="Nombre de présences",
            title="📆 Présences par jour",
            labels={"Date": "Date", "Nombre de présences": "Présences"},
            text_auto=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible pour le graphique.")

    st.markdown("---")
    if st.button("📤 Envoyer le rapport du jour par email"):
        with st.spinner("Génération du rapport..."):
            html = generate_presence_report()
            send_email("tonadresse@gmail.com", "📊 Rapport de présence - FaceLogin", html)
        st.success("✅ Rapport envoyé par email !")
