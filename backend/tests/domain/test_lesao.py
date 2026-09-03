import contextlib
import io
import random

from app.domain.jogador import Jogador
from app.domain.partida import Partida
from scripts.data_loader import carregar_campeonato
from tests.domain.test_partida import _clube_completo


def _silencioso(fn):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn()


def test_jogador_novo_nao_esta_lesionado():
    j = Jogador("X", 25, "Defesa", 80)
    assert j.rodadas_lesao == 0
    assert j.lesionado is False
    assert j.disponivel is True


def test_disponivel_cobre_expulso_suspenso_e_lesionado():
    j = Jogador("Y", 25, "Meio-Campo", 80)
    j.expulso = True
    assert j.disponivel is False
    j.expulso = False
    j.jogos_suspensao = 1
    assert j.disponivel is False
    j.jogos_suspensao = 0
    j.rodadas_lesao = 2
    assert j.disponivel is False


def test_gravidade_da_lesao_fica_no_intervalo():
    random.seed(0)
    p = Partida(_clube_completo("A"), _clube_completo("B"))
    for _ in range(200):
        assert 1 <= p._gravidade_lesao() <= 12


def test_lesionado_fica_de_fora_ate_recuperar():
    random.seed(1)
    casa = _clube_completo("Casa")
    fora = _clube_completo("Fora")
    _silencioso(Partida(casa, fora).simular_partida)

    alvo = next(j for j in casa.titulares if j.posicao == "Atacante")
    alvo.rodadas_lesao = 3

    for espera in (2, 1, 0):
        _silencioso(Partida(casa, fora).simular_partida)
        assert alvo.rodadas_lesao == espera
        if espera:
            assert alvo not in casa.titulares

    partidas_antes = alvo.partidas
    _silencioso(Partida(casa, fora).simular_partida)
    assert alvo.partidas > partidas_antes


def test_temporada_tem_lesoes_e_contadores_saudaveis():
    random.seed(3)
    camp = carregar_campeonato()
    with contextlib.redirect_stdout(io.StringIO()):
        while camp.rodada <= len(camp.calendario):
            camp.jogar_rodada()

    eventos_lesao = [
        e
        for p in camp.partidas_jogadas
        for e in p["eventos"]
        if e["tipo"] == "lesao"
    ]
    assert eventos_lesao, "uma temporada inteira sem nenhuma lesão?"

    jogadores = [j for c in camp.clubes for j in c.jogadores]
    assert all(j.rodadas_lesao >= 0 for j in jogadores)
