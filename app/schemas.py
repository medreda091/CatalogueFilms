"""Schémas Pydantic : validation des entrées et format des réponses."""

from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Films ----------


class FilmCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=200)
    realisateur: str = Field(min_length=1, max_length=200)
    annee: int = Field(ge=1895, le=2100)
    genre: str = Field(min_length=1, max_length=100)
    duree_minutes: int = Field(gt=0)
    synopsis: Optional[str] = None


class FilmUpdate(BaseModel):
    titre: Optional[str] = Field(default=None, min_length=1, max_length=200)
    realisateur: Optional[str] = Field(default=None, min_length=1, max_length=200)
    annee: Optional[int] = Field(default=None, ge=1895, le=2100)
    genre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    duree_minutes: Optional[int] = Field(default=None, gt=0)
    synopsis: Optional[str] = None


class NoteOut(BaseModel):
    id: int
    valeur: float
    commentaire: Optional[str]

    class Config:
        from_attributes = True


class FilmOut(BaseModel):
    id: int
    titre: str
    realisateur: str
    annee: int
    genre: str
    duree_minutes: int
    synopsis: Optional[str]
    note_moyenne: Optional[float]
    nombre_notes: int
    favori: bool

    class Config:
        from_attributes = True


# ---------- Notes ----------


class NoteCreate(BaseModel):
    valeur: float = Field(ge=0, le=10)
    commentaire: Optional[str] = None


# ---------- Statistiques ----------


class StatsGenre(BaseModel):
    genre: str
    nombre_films: int
    note_moyenne: Optional[float]
