# services/db_service.py

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
    presences = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                presences.append(row)
    return presences
