"""Routes de l'API : films, notes, favoris et statistiques."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()


# ---------- Films ----------


@router.post("/films", response_model=schemas.FilmOut, status_code=201)
def creer_film(donnees: schemas.FilmCreate, db: Session = Depends(get_db)):
    return crud.creer_film(db, donnees)


@router.get("/films", response_model=List[schemas.FilmOut])
def lister_films(
    recherche: Optional[str] = None,
    genre: Optional[str] = None,
    annee: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud.lister_films(db, recherche=recherche, genre=genre, annee=annee)


@router.get("/films/top", response_model=List[schemas.FilmOut])
def films_les_mieux_notes(limite: int = 10, db: Session = Depends(get_db)):
    return crud.top_films(db, limite=limite)


@router.get("/films/{film_id}", response_model=schemas.FilmOut)
def obtenir_film(film_id: int, db: Session = Depends(get_db)):
    film = crud.obtenir_film(db, film_id)
    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")
    return film


@router.put("/films/{film_id}", response_model=schemas.FilmOut)
def modifier_film(film_id: int, donnees: schemas.FilmUpdate, db: Session = Depends(get_db)):
    film = crud.modifier_film(db, film_id, donnees)
    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")
    return film


@router.delete("/films/{film_id}", status_code=204)
def supprimer_film(film_id: int, db: Session = Depends(get_db)):
    if not crud.supprimer_film(db, film_id):
        raise HTTPException(status_code=404, detail="Film introuvable")


# ---------- Notes ----------


@router.post("/films/{film_id}/notes", response_model=schemas.NoteOut, status_code=201)
def noter_film(film_id: int, donnees: schemas.NoteCreate, db: Session = Depends(get_db)):
    note = crud.ajouter_note(db, film_id, donnees)
    if note is None:
        raise HTTPException(status_code=404, detail="Film introuvable")
    return note


# ---------- Favoris ----------


@router.get("/favoris", response_model=List[schemas.FilmOut])
def lister_favoris(db: Session = Depends(get_db)):
    return crud.lister_favoris(db)


@router.post("/favoris/{film_id}", status_code=204)
def ajouter_favori(film_id: int, db: Session = Depends(get_db)):
    if crud.ajouter_favori(db, film_id) is None:
        raise HTTPException(status_code=404, detail="Film introuvable")


@router.delete("/favoris/{film_id}", status_code=204)
def retirer_favori(film_id: int, db: Session = Depends(get_db)):
    if not crud.retirer_favori(db, film_id):
        raise HTTPException(status_code=404, detail="Film pas en favori")


# ---------- Statistiques ----------


@router.get("/stats/genres", response_model=List[schemas.StatsGenre])
def stats_par_genre(db: Session = Depends(get_db)):
    return crud.stats_par_genre(db)
