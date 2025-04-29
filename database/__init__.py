from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Pour SQLite (local, simple, sans serveur)
DATABASE_URL = "sqlite:///database/users.db"

# Pour MySQL (quand ton serveur sera OK)
# DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/facelogin_db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
