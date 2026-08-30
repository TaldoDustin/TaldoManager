"""Roda uma temporada completa e devolve os resultados como dados (dict).

A camada de dominio (`Campeonato`, `Partida`, ...) foi escrita para um CLI e
usa muito `print`. Aqui a gente executa a simulacao com a saida padrao
silenciada e transforma os objetos em dicionarios prontos para virar JSON.
"""

import io
import random
from contextlib import redirect_stdout

from scripts.data_loader import carregar_campeonato


def _serializar_clube(posicao, clube):
    jogos = clube.vitorias + clube.empates + clube.derrotas
    return {
        "posicao": posicao,
        "clube": clube.nome,
        "pais": clube.pais,
        "pontos": clube.pontos,
        "jogos": jogos,
        "vitorias": clube.vitorias,
        "empates": clube.empates,
        "derrotas": clube.derrotas,
        "gols_marcados": clube.gols_marcados,
        "gols_sofridos": clube.gols_sofridos,
        "saldo_gols": clube.saldo_gols(),
        "forma": list(clube.forma),
    }


def _serializar_jogador(jogador, clube_nome):
    return {
        "nome": jogador.nome,
        "clube": clube_nome,
        "posicao": jogador.posicao,
        "overall": jogador.overall,
        "idade": jogador.idade,
        "partidas": jogador.partidas,
        "gols": jogador.gols,
        "assistencias": jogador.assistencias,
        "nota_media": jogador.nota_media(),
        "melhor_nota": round(jogador.melhor_nota, 2),
        "pior_nota": round(jogador.pior_nota, 2),
        "melhor_em_campo": jogador.melhor_em_campo,
        "hat_tricks": jogador.hat_tricks,
        "clean_sheets": jogador.clean_sheets,
        "amarelos": jogador.amarelos,
        "vermelhos": jogador.vermelhos,
    }


def simular_temporada(seed=None):
    """Executa a temporada inteira e devolve um dict com todos os rankings.

    Se `seed` for informado, a simulacao vira reproduzivel (mesmo resultado
    para o mesmo seed).
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    campeonato = carregar_campeonato()

    with redirect_stdout(io.StringIO()):
        while campeonato.rodada <= len(campeonato.calendario):
            campeonato.jogar_rodada()

    # todos os jogadores + o clube a que pertencem
    jogadores = []
    for clube in campeonato.clubes:
        for jogador in clube.jogadores:
            jogadores.append((jogador, clube.nome))

    def ranking(chave, filtro=None, limite=None):
        itens = sorted(jogadores, key=lambda par: chave(par[0]), reverse=True)
        if filtro is not None:
            itens = [par for par in itens if filtro(par[0])]
        if limite is not None:
            itens = itens[:limite]
        return [_serializar_jogador(j, nome) for j, nome in itens]

    classificacao = [
        _serializar_clube(i, clube)
        for i, clube in enumerate(campeonato.classificacao(), start=1)
    ]

    mvp_lista = ranking(
        lambda j: (
            j.melhor_em_campo,
            j.nota_media(),
            j.gols + j.assistencias,
            j.hat_tricks,
        )
    )

    return {
        "campeonato": campeonato.nome,
        "seed": seed,
        "rodadas": len(campeonato.calendario),
        "campeao": classificacao[0]["clube"] if classificacao else None,
        "classificacao": classificacao,
        "artilharia": ranking(
            lambda j: (j.gols, j.assistencias),
            filtro=lambda j: j.gols > 0,
            limite=20,
        ),
        "assistencias": ranking(
            lambda j: (j.assistencias, j.gols),
            filtro=lambda j: j.assistencias > 0,
            limite=20,
        ),
        "melhores_notas": ranking(
            lambda j: (j.nota_media(), j.melhor_nota, j.melhor_em_campo),
            filtro=lambda j: j.partidas > 0,
            limite=20,
        ),
        "clean_sheets": ranking(
            lambda j: (j.clean_sheets, j.nota_media()),
            filtro=lambda j: j.posicao == "Goleiro" and j.clean_sheets > 0,
            limite=20,
        ),
        "hat_tricks": ranking(
            lambda j: j.hat_tricks,
            filtro=lambda j: j.hat_tricks > 0,
            limite=20,
        ),
        "mvp": mvp_lista[0] if mvp_lista else None,
        "historico": list(campeonato.historico),
        "recordes": campeonato.recordes,
    }
