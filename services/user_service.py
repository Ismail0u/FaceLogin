from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import Utilisateur

def get_all_users():
    with SessionLocal() as db:
        return db.query(Utilisateur).all()

def get_user_by_email(email: str):
    with SessionLocal() as db:
        return db.query(Utilisateur).filter(Utilisateur.email == email).first()

def add_user(nom: str, email: str, role: str = "utilisateur", password: str = "default123"):
    with SessionLocal() as db:
        user = Utilisateur(nom=nom, email=email, role=role, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

def update_user(user_id: int, nom=None, email=None, role=None, password=None):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        if not user:
            return None
        if nom: user.nom = nom
        if email: user.email = email
        if role: user.role = role
        if password: user.password = password
        db.commit()
        return user

def delete_user(user_id: int):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
