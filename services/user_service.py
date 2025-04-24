from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import Utilisateur


# 🔄 Récupérer tous les utilisateurs
def get_all_users():
    with SessionLocal() as db:
        return db.query(Utilisateur).all()


# ➕ Ajouter un nouvel utilisateur
def add_user(nom: str, email: str, role: str = "utilisateur"):
    with SessionLocal() as db:
        user = Utilisateur(nom=nom, email=email, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


# 🔄 Modifier un utilisateur
def update_user(user_id: int, nom: str = None, email: str = None, role: str = None):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        if not user:
            return None
        if nom:
            user.nom = nom
        if email:
            user.email = email
        if role:
            user.role = role
        db.commit()
        return user


# ❌ Supprimer un utilisateur
def delete_user(user_id: int):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
