"""Tests de l'API films : création, lecture, modification, suppression, recherche."""


def test_creer_un_film(client):
    reponse = client.post(
        "/films",
        json={
            "titre": "Intouchables",
            "realisateur": "Olivier Nakache",
            "annee": 2011,
            "genre": "Comédie",
            "duree_minutes": 112,
        },
    )
    assert reponse.status_code == 201
    donnees = reponse.json()
    assert donnees["titre"] == "Intouchables"
    assert donnees["favori"] is False
    assert donnees["note_moyenne"] is None


def test_refuse_un_film_invalide(client):
    # Année impossible
    reponse = client.post(
        "/films",
        json={
            "titre": "X",
            "realisateur": "Y",
            "annee": 1700,
            "genre": "Z",
            "duree_minutes": 90,
        },
    )
    assert reponse.status_code == 422


def test_lire_un_film(client, film_exemple):
    reponse = client.get(f"/films/{film_exemple['id']}")
    assert reponse.status_code == 200
    assert reponse.json()["titre"] == "Le Fabuleux Destin d'Amélie Poulain"


def test_film_introuvable(client):
    reponse = client.get("/films/99999")
    assert reponse.status_code == 404


def test_modifier_un_film(client, film_exemple):
    reponse = client.put(
        f"/films/{film_exemple['id']}",
        json={"genre": "Comédie romantique"},
    )
    assert reponse.status_code == 200
    assert reponse.json()["genre"] == "Comédie romantique"
    assert reponse.json()["titre"] == film_exemple["titre"]


def test_rechercher_un_film(client, film_exemple):
    reponse = client.get("/films", params={"recherche": "amélie"})
    assert reponse.status_code == 200
    titres = [f["titre"] for f in reponse.json()]
    assert film_exemple["titre"] in titres


def test_filtrer_par_genre(client, film_exemple):
    reponse = client.get("/films", params={"genre": "Comédie"})
    assert reponse.status_code == 200
    assert all(f["genre"].lower() == "comédie" for f in reponse.json())


def test_supprimer_un_film(client, film_exemple):
    reponse = client.delete(f"/films/{film_exemple['id']}")
    assert reponse.status_code == 204
    assert client.get(f"/films/{film_exemple['id']}").status_code == 404
