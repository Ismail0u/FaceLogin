# init_db.py

from database import engine, SessionLocal
from models.user_model import Base, Utilisateur

# Création des tables
Base.metadata.create_all(bind=engine)
print("✅ Tables créées.")

# Création d'un admin par défaut
def create_admin():
    with SessionLocal() as db:
        existing = db.query(Utilisateur).filter(Utilisateur.email == "admin@email.com").first()
        if existing:
            print("ℹ️ Admin déjà présent.")
            return
        admin = Utilisateur(
            nom="Administrateur",
            email="admin@email.com",
            password="admin123",  # Tu pourras améliorer ça avec du hash plus tard
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("✅ Admin ajouté : admin@email.com / admin123")

# Exécution
if __name__ == "__main__":
    create_admin()
