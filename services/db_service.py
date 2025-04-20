# services/db_service.py
import ast  # pour parser la chaîne de dictionnaire
import os
import csv
from datetime import datetime

CSV_PATH = "database/presence_log.csv"

# Initialisation du fichier CSV s’il n'existe pas
def init_csv():
    if not os.path.exists(os.path.dirname(CSV_PATH)):
        os.makedirs(os.path.dirname(CSV_PATH))

    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "date", "time"])

# Enregistre une présence dans le CSV
def log_presence(name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    with open(CSV_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, date_str, time_str])

# Récupère toutes les présences (en option : filtrer par nom ou date)
def get_all_presences():
    if not os.path.exists(CSV_PATH):
        return []

    cleaned_data = []
    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                identity_dict = ast.literal_eval(row[0])
                name = identity_dict.get("identity", "Inconnu")
                date = row[1]
                time = row[2]
                cleaned_data.append({
                    "Nom": name,
                    "Date": date,
                    "Heure": time,
                    "DateTime": datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                print("Erreur:", e)
    return cleaned_data