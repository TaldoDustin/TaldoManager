from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_simulacao_responde_no_formato_do_schema():
    resp = client.get("/simulacao?seed=5")
    assert resp.status_code == 200

    corpo = resp.json()
    assert corpo["seed"] == 5
    assert corpo["rodadas"] == 38
    assert len(corpo["classificacao"]) == 20
    assert corpo["campeao"] == corpo["classificacao"][0]["clube"]
    assert corpo["mvp"] is not None


def test_simulacao_sem_seed_funciona():
    resp = client.get("/simulacao")
    assert resp.status_code == 200
    assert resp.json()["seed"] is None
