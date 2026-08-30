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
