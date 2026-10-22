"""Configuration pytest : base SQLite en mémoire pour les tests."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import pytest

# Le dossier du projet doit être importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    # Chaque test repart d'une base vide : isole les tests entre eux.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def session_de_test():
        db = SessionTest()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = session_de_test
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def film_exemple(client):
    reponse = client.post(
        "/films",
        json={
            "titre": "Le Fabuleux Destin d'Amélie Poulain",
            "realisateur": "Jean-Pierre Jeunet",
            "annee": 2001,
            "genre": "Comédie",
            "duree_minutes": 122,
            "synopsis": "Amélie décide de changer la vie des gens autour d'elle.",
        },
    )
    assert reponse.status_code == 201
    return reponse.json()
