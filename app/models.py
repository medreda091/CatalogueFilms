"""Modèles SQLAlchemy : films, notes et favoris."""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Film(Base):
    """Un film du catalogue."""

    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False, index=True)
    realisateur = Column(String(200), nullable=False, index=True)
    annee = Column(Integer, nullable=False)
    genre = Column(String(100), nullable=False, index=True)
    duree_minutes = Column(Integer, nullable=False)
    synopsis = Column(Text, nullable=True)

    notes = relationship("Note", back_populates="film", cascade="all, delete-orphan")
    favoris = relationship("Favori", back_populates="film", cascade="all, delete-orphan")

    @property
    def note_moyenne(self):
        """Moyenne des notes reçues, arrondie à 1 décimale (None si aucune)."""
        if not self.notes:
            return None
        return round(sum(n.valeur for n in self.notes) / len(self.notes), 1)


class Note(Base):
    """Une note (1 à 10) donnée à un film, avec un commentaire optionnel."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), nullable=False)
    valeur = Column(Float, nullable=False)
    commentaire = Column(Text, nullable=True)

    film = relationship("Film", back_populates="notes")


class Favori(Base):
    """Un film marqué en favori."""

    __tablename__ = "favoris"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), nullable=False, unique=True)

    film = relationship("Film", back_populates="favoris")
