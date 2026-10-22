# CatalogueFilms

Une API REST pour cataloguer ses films : ajouter des films, les noter, lancer
des recherches, marquer ses favoris et consulter des statistiques (top des films,
moyennes par genre).

## Stack

- Python 3.12, FastAPI, SQLAlchemy 2
- PostgreSQL 16 (via Docker), Pydantic
- pytest pour les tests, GitHub Actions pour la CI

## Installation

### Avec Docker (recommandé)

```bash
cp .env.example .env
docker compose up --build
```

L'API est disponible sur http://localhost:8000, la documentation interactive
sur http://localhost:8000/docs.

### En local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # puis renseigne ta DATABASE_URL
uvicorn app.main:app --reload
```

## Utilisation

```bash
# Ajouter un film
curl -X POST http://localhost:8000/films -H "Content-Type: application/json" -d '{
  "titre": "Intouchables",
  "realisateur": "Olivier Nakache",
  "annee": 2011,
  "genre": "Comédie",
  "duree_minutes": 112
}'

# Rechercher un film (titre, réalisateur ou synopsis)
curl "http://localhost:8000/films?recherche=amelie"

# Filtrer par genre et année
curl "http://localhost:8000/films?genre=Comédie&annee=2011"

# Noter un film (0 à 10)
curl -X POST http://localhost:8000/films/1/notes -H "Content-Type: application/json" -d '{
  "valeur": 9,
  "commentaire": "Un classique."
}'

# Ajouter aux favoris, puis lister ses favoris
curl -X POST http://localhost:8000/favoris/1
curl http://localhost:8000/favoris

# Top des films les mieux notés
curl http://localhost:8000/films/top?limite=5

# Statistiques par genre
curl http://localhost:8000/stats/genres
```

## Structure du projet

```
CatalogueFilms/
├── app/
│   ├── main.py          # point d'entrée FastAPI
│   ├── database.py      # connexion à la base (SQLAlchemy)
│   ├── models.py        # modèles : Film, Note, Favori
│   ├── schemas.py       # validation Pydantic
│   ├── crud.py          # accès aux données
│   └── routers/
│       └── films.py     # routes films, notes, favoris, stats
├── tests/               # tests pytest (SQLite en mémoire)
├── Dockerfile
├── docker-compose.yml   # API + PostgreSQL
└── .github/workflows/ci.yml
```

## Tests

```bash
pytest tests/ -q
```

16 tests couvrent le CRUD des films, la recherche et les filtres, les notes
(avec la moyenne), les favoris et les statistiques.

## Licence

MIT
