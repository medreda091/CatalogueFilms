"""Point d'entrée de l'API CatalogueFilms."""

from fastapi import FastAPI

from .database import Base, engine
from .routers.films import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CatalogueFilms",
    description="API pour cataloguer ses films : notes, recherche, favoris et statistiques.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API CatalogueFilms", "docs": "/docs"}
