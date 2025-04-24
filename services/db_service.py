# services/db_service.py
import ast
import os
import csv
from datetime import datetime

# Chemin vers le fichier CSV de présence
CSV_PATH = "database/presence_log.csv"

# Initialise le dossier et le fichier CSV avec en-têtes si nécessaire
def init_csv():
    directory = os.path.dirname(CSV_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["name", "date", "time"])  # en-têtes

# Enregistre une présence dans le CSV
def log_presence(name: str):
    init_csv()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, date_str, time_str])

# Récupère et nettoie toutes les présences
def get_all_presences():
    init_csv()
    presences = []
    with open(CSV_PATH, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # sauter l'en-tête
        for row in reader:
            if len(row) < 3:
                continue  # ignore les lignes corrompues
            raw, date_str, time_str = row[0].strip(), row[1].strip(), row[2].strip()
            # Essayer de parser une dict-string {'identity': 'Name'}
            name = raw
            if raw.startswith("{") and raw.endswith("}"):
                try:
                    parsed = ast.literal_eval(raw)
                    if isinstance(parsed, dict) and "identity" in parsed:
                        name = parsed["identity"]
                except (ValueError, SyntaxError):
                    # si parsing échoue, conserver raw
                    pass
            presences.append({
                "Nom": name,
                "Date": date_str,
                "Heure": time_str,
            })
    return presences
