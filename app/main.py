"""Point d'entrée de l'API CatalogueFilms."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers.films import router


@asynccontextmanager
async def cycle_de_vie(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        # En test, la base réelle n'est pas forcément joignable : les tests
        # utilisent leur propre session via la dépendance surchargée.
        pass
    yield


app = FastAPI(
    title="CatalogueFilms",
    description="API pour cataloguer ses films : notes, recherche, favoris et statistiques.",
    version="1.0.0",
    lifespan=cycle_de_vie,
)

app.include_router(router)


@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API CatalogueFilms", "docs": "/docs"}
