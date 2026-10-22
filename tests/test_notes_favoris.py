"""Tests des notes, favoris et statistiques."""


def test_ajouter_une_note(client, film_exemple):
    reponse = client.post(
        f"/films/{film_exemple['id']}/notes",
        json={"valeur": 9, "commentaire": "Un classique."},
    )
    assert reponse.status_code == 201
    assert reponse.json()["valeur"] == 9


def test_note_hors_limites_refusee(client, film_exemple):
    reponse = client.post(
        f"/films/{film_exemple['id']}/notes",
        json={"valeur": 15},
    )
    assert reponse.status_code == 422


def test_note_moyenne_calculee(client, film_exemple):
    client.post(f"/films/{film_exemple['id']}/notes", json={"valeur": 8})
    client.post(f"/films/{film_exemple['id']}/notes", json={"valeur": 10})
    reponse = client.get(f"/films/{film_exemple['id']}")
    donnees = reponse.json()
    assert donnees["note_moyenne"] == 9.0
    assert donnees["nombre_notes"] == 2


def test_ajouter_et_lister_favoris(client, film_exemple):
    reponse = client.post(f"/favoris/{film_exemple['id']}")
    assert reponse.status_code == 204

    reponse = client.get("/favoris")
    assert reponse.status_code == 200
    assert any(f["id"] == film_exemple["id"] for f in reponse.json())

    # Le film est marqué favori dans sa fiche
    reponse = client.get(f"/films/{film_exemple['id']}")
    assert reponse.json()["favori"] is True


def test_retirer_favori(client, film_exemple):
    client.post(f"/favoris/{film_exemple['id']}")
    reponse = client.delete(f"/favoris/{film_exemple['id']}")
    assert reponse.status_code == 204
    assert client.get("/favoris").json() == []


def test_favori_sur_film_inexistant(client):
    assert client.post("/favoris/99999").status_code == 404


def test_top_films(client, film_exemple):
    client.post(f"/films/{film_exemple['id']}/notes", json={"valeur": 9})
    reponse = client.get("/films/top")
    assert reponse.status_code == 200
    assert len(reponse.json()) >= 1
    assert reponse.json()[0]["id"] == film_exemple["id"]


def test_stats_par_genre(client, film_exemple):
    client.post(f"/films/{film_exemple['id']}/notes", json={"valeur": 8})
    reponse = client.get("/stats/genres")
    assert reponse.status_code == 200
    genres = {s["genre"]: s for s in reponse.json()}
    assert "Comédie" in genres
    assert genres["Comédie"]["nombre_films"] >= 1
    assert genres["Comédie"]["note_moyenne"] == 8.0
