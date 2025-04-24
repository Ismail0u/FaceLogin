# services/report_service.py

import pandas as pd
from services.db_service import get_all_presences
from datetime import datetime, timedelta

def generate_presence_report():
    data = get_all_presences()
    df = pd.DataFrame(data, columns=["Nom", "Date", "Heure"])
    df["Date"] = pd.to_datetime(df["Date"])

    today = pd.Timestamp(datetime.datetime.now().date())
    weekday = today.strftime("%A")

    report_html = f"<h2>📅 Rapport du {today.strftime('%d/%m/%Y')} ({weekday})</h2>"

    # Présences du jour
    today_df = df[df["Date"] == today]
    if not today_df.empty:
        report_html += f"<p>👥 <strong>{len(today_df)}</strong> présences aujourd’hui :</p><ul>"
        for name in today_df["Nom"].unique():
            report_html += f"<li>{name}</li>"
        report_html += "</ul>"
    else:
        report_html += "<p>🚫 <strong>Aucune présence enregistrée aujourd’hui.</strong></p>"

    # Statistiques globales
    total_users = df["Nom"].nunique()
    total_days = df["Date"].nunique()
    report_html += f"<hr><p>📈 Total utilisateurs : {total_users}</p>"
    report_html += f"<p>📆 Jours avec présence : {total_days}</p>"

    return report_html

from io import BytesIO
from fpdf import FPDF

from fpdf import FPDF
from io import BytesIO
import datetime

def generate_pdf_report(filtered_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Rapport des présences", ln=True, align="C")
    pdf.ln(10)

    for _, row in filtered_df.iterrows():
        line = f"{row['Nom']} - {row['Date']} à {row['Heure']}"
        pdf.cell(200, 10, txt=line, ln=True)

    # ✅ Générer en mémoire
    pdf_output = pdf.output(dest="S").encode("latin1")  # encode le PDF en bytes
    return BytesIO(pdf_output)  # renvoie un objet BytesIO compatible Streamlit
