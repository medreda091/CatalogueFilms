"""Accès aux données : films, notes et favoris."""

from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def enrichir_film(film: models.Film) -> dict:
    """Ajoute les champs calculés (note moyenne, nombre de notes, favori)."""
    return {
        "id": film.id,
        "titre": film.titre,
        "realisateur": film.realisateur,
        "annee": film.annee,
        "genre": film.genre,
        "duree_minutes": film.duree_minutes,
        "synopsis": film.synopsis,
        "note_moyenne": film.note_moyenne,
        "nombre_notes": len(film.notes),
        "favori": len(film.favoris) > 0,
    }


# ---------- Films ----------


def creer_film(db: Session, donnees: schemas.FilmCreate) -> dict:
    film = models.Film(**donnees.model_dump())
    db.add(film)
    db.commit()
    db.refresh(film)
    return enrichir_film(film)


def lister_films(
    db: Session,
    recherche: Optional[str] = None,
    genre: Optional[str] = None,
    annee: Optional[int] = None,
) -> List[dict]:
    """Liste les films, avec recherche plein texte simple et filtres."""
    query = db.query(models.Film)
    if recherche:
        motif = f"%{recherche}%"
        query = query.filter(
            (models.Film.titre.ilike(motif))
            | (models.Film.realisateur.ilike(motif))
            | (models.Film.synopsis.ilike(motif))
        )
    if genre:
        query = query.filter(models.Film.genre.ilike(genre))
    if annee:
        query = query.filter(models.Film.annee == annee)
    return [enrichir_film(f) for f in query.order_by(models.Film.titre).all()]


def obtenir_film(db: Session, film_id: int) -> Optional[dict]:
    film = db.query(models.Film).filter(models.Film.id == film_id).first()
    return enrichir_film(film) if film else None


def modifier_film(db: Session, film_id: int, donnees: schemas.FilmUpdate) -> Optional[dict]:
    film = db.query(models.Film).filter(models.Film.id == film_id).first()
    if not film:
        return None
    for champ, valeur in donnees.model_dump(exclude_unset=True).items():
        setattr(film, champ, valeur)
    db.commit()
    db.refresh(film)
    return enrichir_film(film)


def supprimer_film(db: Session, film_id: int) -> bool:
    film = db.query(models.Film).filter(models.Film.id == film_id).first()
    if not film:
        return False
    db.delete(film)
    db.commit()
    return True


# ---------- Notes ----------


def ajouter_note(db: Session, film_id: int, donnees: schemas.NoteCreate) -> Optional[dict]:
    film = db.query(models.Film).filter(models.Film.id == film_id).first()
    if not film:
        return None
    note = models.Note(film_id=film_id, **donnees.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"id": note.id, "valeur": note.valeur, "commentaire": note.commentaire}


# ---------- Favoris ----------


def lister_favoris(db: Session) -> List[dict]:
    favoris = db.query(models.Film).join(models.Favori).order_by(models.Film.titre).all()
    return [enrichir_film(f) for f in favoris]


def ajouter_favori(db: Session, film_id: int) -> Optional[bool]:
    film = db.query(models.Film).filter(models.Film.id == film_id).first()
    if not film:
        return None
    existe = db.query(models.Favori).filter(models.Favori.film_id == film_id).first()
    if existe:
        return True
    db.add(models.Favori(film_id=film_id))
    db.commit()
    return True


def retirer_favori(db: Session, film_id: int) -> bool:
    favori = db.query(models.Favori).filter(models.Favori.film_id == film_id).first()
    if not favori:
        return False
    db.delete(favori)
    db.commit()
    return True


# ---------- Statistiques ----------


def top_films(db: Session, limite: int = 10) -> List[dict]:
    """Films les mieux notés (au moins une note), triés par moyenne décroissante."""
    films = db.query(models.Film).all()
    notes = [enrichir_film(f) for f in films if f.notes]
    notes.sort(key=lambda f: (f["note_moyenne"] or 0, f["nombre_notes"]), reverse=True)
    return notes[:limite]


def stats_par_genre(db: Session) -> List[dict]:
    """Nombre de films et note moyenne par genre."""
    films = db.query(models.Film).all()
    agregats: dict = {}
    for f in films:
        g = agregats.setdefault(f.genre, {"nombre": 0, "somme": 0.0, "notes": 0})
        g["nombre"] += 1
        if f.note_moyenne is not None:
            g["somme"] += f.note_moyenne
            g["notes"] += 1
    resultat = []
    for genre, g in sorted(agregats.items()):
        moyenne = round(g["somme"] / g["notes"], 1) if g["notes"] else None
        resultat.append({"genre": genre, "nombre_films": g["nombre"], "note_moyenne": moyenne})
    return resultat
