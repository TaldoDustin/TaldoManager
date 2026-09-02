import pytest

from app.db.conexao import conectar
from app.repositories import clube_repository as clube_repo
from app.repositories import jogador_repository as jogador_repo
from app.repositories import partida_repository as partida_repo
from app.repositories import simulacao_repository as simulacao_repo


@pytest.fixture
def conn():
    c = conectar()
    yield c
    c.close()


def _clube(nome, posicao):
    return {
        "nome": nome, "pais": "Brasil", "posicao_final": posicao,
        "pontos": 90 - posicao, "jogos": 38, "vitorias": 20,
        "empates": 10, "derrotas": 8, "gols_marcados": 60, "gols_sofridos": 40,
    }


def _jogador(nome, clube):
    return {
        "clube": clube, "nome": nome, "posicao": "Atacante", "idade": 25,
        "overall": 82, "partidas": 38, "gols": 15, "assistencias": 5,
        "nota_media": 7.4, "melhor_nota": 9.1, "pior_nota": 5.2,
        "melhor_em_campo": 8, "clean_sheets": 0, "hat_tricks": 1,
        "amarelos": 3, "vermelhos": 0,
    }


def test_ciclo_completo_de_escrita_e_leitura(conn):
    with conn:
        sid = simulacao_repo.criar(
            conn, seed=7, campeao="A FC", rodadas=38, criada_em="2026-01-01"
        )
        mapa = clube_repo.inserir(conn, sid, [_clube("A FC", 1), _clube("B FC", 2)])
        jogador_repo.inserir(
            conn, sid, mapa, [_jogador("Craque", "A FC"), _jogador("Outro", "B FC")]
        )
        partida_repo.inserir(conn, sid, mapa, [{
            "rodada": 1, "mandante": "A FC", "visitante": "B FC",
            "gols_mandante": 3, "gols_visitante": 1, "posse_mandante": 60,
            "finalizacoes_mandante": 12, "finalizacoes_visitante": 6,
        }])

    assert len(mapa) == 2

    clubes = clube_repo.listar_por_simulacao(conn, sid)
    assert [c["nome"] for c in clubes] == ["A FC", "B FC"]  # ordena por posição

    elenco = jogador_repo.listar_por_clube(conn, mapa["A FC"])
    assert len(elenco) == 1
    assert elenco[0]["nome"] == "Craque"
    assert elenco[0]["clube"] == "A FC"  # veio pelo JOIN

    jogos = partida_repo.listar_por_clube(conn, mapa["B FC"])
    assert len(jogos) == 1
    assert jogos[0]["mandante_nome"] == "A FC"
    assert jogos[0]["visitante_nome"] == "B FC"


def test_deletar_simulacao_apaga_em_cascata(conn):
    with conn:
        sid = simulacao_repo.criar(
            conn, seed=None, campeao="A FC", rodadas=38, criada_em="2026-01-01"
        )
        mapa = clube_repo.inserir(conn, sid, [_clube("A FC", 1)])
        jogador_repo.inserir(conn, sid, mapa, [_jogador("Craque", "A FC")])

    with conn:
        assert simulacao_repo.deletar(conn, sid) is True

    assert clube_repo.listar_por_simulacao(conn, sid) == []
    assert jogador_repo.listar_por_simulacao(conn, sid) == []
    assert simulacao_repo.buscar(conn, sid) is None


def test_deletar_simulacao_inexistente(conn):
    with conn:
        assert simulacao_repo.deletar(conn, 999) is False
