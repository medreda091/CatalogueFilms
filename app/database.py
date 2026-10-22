"""Configuration de la connexion à la base de données."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Utilisée par défaut en local via docker-compose, surchargeable avec un .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://catalogue:catalogue@localhost:5432/catalogue_films",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dépendance FastAPI : fournit une session puis la referme."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
