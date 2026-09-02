from app.services import simulacao_service
from app.services.simulacao_service import simular_temporada


def test_simulacao_tem_todas_as_chaves():
    r = simular_temporada(seed=1)

    esperadas = {
        "campeonato", "seed", "rodadas", "campeao", "classificacao",
        "artilharia", "assistencias", "melhores_notas", "clean_sheets",
        "hat_tricks", "mvp", "historico", "recordes",
    }
    assert esperadas <= set(r)


def test_classificacao_completa_e_ordenada():
    r = simular_temporada(seed=1)

    assert len(r["classificacao"]) == 20
    pontos = [c["pontos"] for c in r["classificacao"]]
    assert pontos == sorted(pontos, reverse=True)
    assert r["classificacao"][0]["clube"] == r["campeao"]


def test_todos_os_clubes_jogaram_todas_as_rodadas():
    r = simular_temporada(seed=1)

    assert r["rodadas"] == 38
    assert len(r["historico"]) == 380
    for clube in r["classificacao"]:
        assert clube["jogos"] == 38


def test_seed_torna_a_simulacao_reproduzivel():
    a = simular_temporada(seed=99)
    b = simular_temporada(seed=99)

    assert a["classificacao"] == b["classificacao"]
    assert a["artilharia"] == b["artilharia"]


def test_rankings_respeitam_os_filtros():
    r = simular_temporada(seed=1)

    assert all(j["gols"] > 0 for j in r["artilharia"])
    assert all(j["assistencias"] > 0 for j in r["assistencias"])
    assert all(j["posicao"] == "Goleiro" for j in r["clean_sheets"])


# --- persistência ---

def test_salvar_e_carregar_devolve_a_mesma_visao():
    sid = simulacao_service.salvar_temporada(seed=42)

    salva = simulacao_service.carregar_temporada(sid)
    fresca = simular_temporada(seed=42)

    def resumo(v):
        return (
            [(c["posicao"], c["clube"], c["pontos"], c["saldo_gols"], c["forma"])
             for c in v["classificacao"]],
            [(j["nome"], j["gols"], j["assistencias"]) for j in v["artilharia"]],
            v["campeao"],
            v["recordes"],
            v["historico"],
        )

    assert resumo(salva) == resumo(fresca)


def test_simulacao_salva_ganha_ids_para_navegacao():
    sid = simulacao_service.salvar_temporada(seed=42)
    salva = simulacao_service.carregar_temporada(sid)

    assert all(isinstance(c["id"], int) for c in salva["classificacao"])
    assert all(isinstance(j["id"], int) for j in salva["artilharia"])

    # modo rápido não persiste, então não tem id
    assert simular_temporada(seed=42)["classificacao"][0]["id"] is None


def test_listar_e_apagar_simulacoes():
    assert simulacao_service.listar_simulacoes() == []

    a = simulacao_service.salvar_temporada(seed=1)
    b = simulacao_service.salvar_temporada(seed=2)

    lista = simulacao_service.listar_simulacoes()
    assert {s["id"] for s in lista} == {a, b}
    assert all({"seed", "criada_em", "campeao", "rodadas"} <= set(s) for s in lista)

    assert simulacao_service.apagar_simulacao(a) is True
    assert {s["id"] for s in simulacao_service.listar_simulacoes()} == {b}
    assert simulacao_service.apagar_simulacao(a) is False


def test_carregar_simulacao_inexistente():
    assert simulacao_service.carregar_temporada(999) is None


def test_detalhe_clube():
    sid = simulacao_service.salvar_temporada(seed=42)
    campeao_id = simulacao_service.carregar_temporada(sid)["classificacao"][0]["id"]

    det = simulacao_service.detalhe_clube(sid, campeao_id)

    assert len(det["elenco"]) == 18
    assert len(det["jogos"]) == 38
    assert det["clube"]["posicao_final"] == 1
    # pontos batem com o aproveitamento nos jogos
    v = sum(1 for j in det["jogos"] if j["resultado"] == "V")
    e = sum(1 for j in det["jogos"] if j["resultado"] == "E")
    assert det["clube"]["pontos"] == v * 3 + e


def test_detalhe_clube_de_outra_simulacao_da_none():
    sid = simulacao_service.salvar_temporada(seed=1)
    clube_id = simulacao_service.carregar_temporada(sid)["classificacao"][0]["id"]

    assert simulacao_service.detalhe_clube(999, clube_id) is None
