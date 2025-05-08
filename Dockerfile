# Base image avec Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exposer le port de Streamlit
EXPOSE 8501

# Commande de lancement
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
