from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Remplace par tes vrais identifiants MySQL
DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/facelogin_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
