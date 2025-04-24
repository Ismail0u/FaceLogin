from services.db_service import get_all_presences
from services.report_service import generate_presence_report
from services.email_service import send_email

def send_daily_report():
    data = get_all_presences()
    if not data:
        print("Aucune présence aujourd’hui.")
        return

    html = generate_presence_report()
    send_email("tonemail@exemple.com", "📊 Rapport quotidien - FaceLogin", html)
    print("✅ Rapport envoyé avec succès.")

if __name__ == "__main__":
    send_daily_report()
