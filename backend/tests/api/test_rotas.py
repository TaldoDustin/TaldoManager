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


# --- simulações persistidas ---

def test_fluxo_criar_listar_obter_apagar():
    assert client.get("/simulacoes").json() == []

    criada = client.post("/simulacoes?seed=42")
    assert criada.status_code == 201
    sid = criada.json()["id"]

    lista = client.get("/simulacoes").json()
    assert len(lista) == 1
    assert lista[0]["id"] == sid
    assert lista[0]["campeao"]

    obtida = client.get(f"/simulacoes/{sid}")
    assert obtida.status_code == 200
    corpo = obtida.json()
    assert len(corpo["classificacao"]) == 20
    assert corpo["classificacao"][0]["id"] is not None

    assert client.delete(f"/simulacoes/{sid}").status_code == 204
    assert client.get("/simulacoes").json() == []


def test_obter_simulacao_inexistente_404():
    assert client.get("/simulacoes/999").status_code == 404
    assert client.delete("/simulacoes/999").status_code == 404


def test_detalhe_do_clube():
    sid = client.post("/simulacoes?seed=42").json()["id"]
    campeao = client.get(f"/simulacoes/{sid}").json()["classificacao"][0]
    cid = campeao["id"]

    resp = client.get(f"/simulacoes/{sid}/clubes/{cid}")
    assert resp.status_code == 200

    corpo = resp.json()
    assert corpo["clube"]["nome"] == campeao["clube"]
    assert len(corpo["elenco"]) == 18
    assert len(corpo["jogos"]) == 38

    assert client.get(f"/simulacoes/{sid}/clubes/9999").status_code == 404
