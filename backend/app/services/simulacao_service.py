"""Roda uma temporada e transforma o resultado em dados (dict/JSON).

Três caminhos:
- `simular_temporada`  -> roda e devolve a visão, sem tocar no banco (modo rápido)
- `salvar_temporada`   -> roda e persiste; devolve o id da simulação
- `carregar_temporada` -> lê do banco e devolve a mesma visão

A visão (classificação, rankings, recordes, ...) é sempre montada por
`_montar_visao`, então os três caminhos produzem o mesmo formato.
"""

import io
import random
from contextlib import redirect_stdout
from datetime import datetime, timezone

from app.db.conexao import conectar
from app.repositories import atuacao_repository as atuacao_repo
from app.repositories import clube_repository as clube_repo
from app.repositories import jogador_repository as jogador_repo
from app.repositories import lance_repository as lance_repo
from app.repositories import partida_repository as partida_repo
from app.repositories import simulacao_repository as simulacao_repo
from scripts.data_loader import carregar_campeonato

NOME_CAMPEONATO = "Taldo"


# ---------------------------------------------------------------------------
# rodar a simulação
# ---------------------------------------------------------------------------

def _rodar(seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    campeonato = carregar_campeonato()

    with redirect_stdout(io.StringIO()):
        while campeonato.rodada <= len(campeonato.calendario):
            campeonato.jogar_rodada()

    return campeonato


# ---------------------------------------------------------------------------
# dados crus (o que vai pro banco)
# ---------------------------------------------------------------------------

def _serializar_jogador(jogador, clube_nome):
    return {
        "id": None,          # preenchido só quando vem do banco
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


def _serializar(campeonato, seed):
    classificacao = campeonato.classificacao()
    posicao = {c.nome: i for i, c in enumerate(classificacao, start=1)}

    clubes = []
    jogadores = []

    for clube in campeonato.clubes:
        jogos = clube.vitorias + clube.empates + clube.derrotas
        clubes.append({
            "nome": clube.nome,
            "pais": clube.pais,
            "posicao_final": posicao[clube.nome],
            "pontos": clube.pontos,
            "jogos": jogos,
            "vitorias": clube.vitorias,
            "empates": clube.empates,
            "derrotas": clube.derrotas,
            "gols_marcados": clube.gols_marcados,
            "gols_sofridos": clube.gols_sofridos,
        })

        for jogador in clube.jogadores:
            jogadores.append(_serializar_jogador(jogador, clube.nome))

    return {
        "seed": seed,
        "campeao": classificacao[0].nome,
        "rodadas": len(campeonato.calendario),
        "clubes": clubes,
        "jogadores": jogadores,
        "partidas": list(campeonato.partidas_jogadas),
    }


# ---------------------------------------------------------------------------
# montar a visão a partir dos dados crus
# ---------------------------------------------------------------------------

def _forma_por_clube(partidas):
    """Últimos 5 resultados de cada clube (V/E/D), em ordem cronológica."""
    forma = {}
    for p in sorted(partidas, key=lambda x: x["rodada"]):
        for clube, pro, contra in (
            (p["mandante"], p["gols_mandante"], p["gols_visitante"]),
            (p["visitante"], p["gols_visitante"], p["gols_mandante"]),
        ):
            r = "V" if pro > contra else "D" if pro < contra else "E"
            forma.setdefault(clube, []).append(r)
    return {clube: r[-5:] for clube, r in forma.items()}


def _recordes(partidas):
    maior_goleada = {"valor": 0, "partida": ""}
    mais_gols = {"valor": 0, "partida": ""}

    for p in partidas:
        desc = (
            f"{p['mandante']} {p['gols_mandante']} x "
            f"{p['gols_visitante']} {p['visitante']}"
        )
        dif = abs(p["gols_mandante"] - p["gols_visitante"])
        total = p["gols_mandante"] + p["gols_visitante"]

        if dif > maior_goleada["valor"]:
            maior_goleada = {"valor": dif, "partida": desc}
        if total > mais_gols["valor"]:
            mais_gols = {"valor": total, "partida": desc}

    return {"maior_goleada": maior_goleada, "mais_gols_jogo": mais_gols}


def _evolucao_pontos(partidas, clubes_ordenados):
    """Pontos acumulados de cada clube ao fim de cada rodada (para o gráfico
    da corrida pelo título). `clubes_ordenados` já vem na ordem da tabela."""

    rodadas = sorted({p["rodada"] for p in partidas})

    ganho = {c["nome"]: dict.fromkeys(rodadas, 0) for c in clubes_ordenados}

    for p in partidas:
        gm, gv = p["gols_mandante"], p["gols_visitante"]
        if gm > gv:
            ganho[p["mandante"]][p["rodada"]] += 3
        elif gv > gm:
            ganho[p["visitante"]][p["rodada"]] += 3
        else:
            ganho[p["mandante"]][p["rodada"]] += 1
            ganho[p["visitante"]][p["rodada"]] += 1

    series = []
    for c in clubes_ordenados:
        acumulado = 0
        pontos = []
        for r in rodadas:
            acumulado += ganho[c["nome"]][r]
            pontos.append(acumulado)
        series.append({"clube": c["nome"], "id": c.get("id"), "pontos": pontos})

    return {"rodadas": rodadas, "series": series}


def _montar_visao(cru):
    partidas = cru["partidas"]
    forma = _forma_por_clube(partidas)

    clubes_ordenados = sorted(cru["clubes"], key=lambda c: c["posicao_final"])

    classificacao = [
        {
            "id": c.get("id"),
            "posicao": c["posicao_final"],
            "clube": c["nome"],
            "pais": c["pais"],
            "pontos": c["pontos"],
            "jogos": c["jogos"],
            "vitorias": c["vitorias"],
            "empates": c["empates"],
            "derrotas": c["derrotas"],
            "gols_marcados": c["gols_marcados"],
            "gols_sofridos": c["gols_sofridos"],
            "saldo_gols": c["gols_marcados"] - c["gols_sofridos"],
            "forma": forma.get(c["nome"], []),
        }
        for c in clubes_ordenados
    ]

    jogadores = cru["jogadores"]

    def ranking(chave, filtro=None, limite=None):
        itens = sorted(jogadores, key=chave, reverse=True)
        if filtro is not None:
            itens = [j for j in itens if filtro(j)]
        if limite is not None:
            itens = itens[:limite]
        return itens

    mvp_lista = ranking(
        lambda j: (
            j["melhor_em_campo"],
            j["nota_media"],
            j["gols"] + j["assistencias"],
            j["hat_tricks"],
        )
    )

    historico = [
        f"Rodada {p['rodada']}: {p['mandante']} "
        f"{p['gols_mandante']} x {p['gols_visitante']} {p['visitante']}"
        for p in sorted(partidas, key=lambda x: x["rodada"])
    ]

    return {
        "campeonato": NOME_CAMPEONATO,
        "seed": cru["seed"],
        "rodadas": cru["rodadas"],
        "campeao": cru["campeao"],
        "classificacao": classificacao,
        "artilharia": ranking(
            lambda j: (j["gols"], j["assistencias"]),
            filtro=lambda j: j["gols"] > 0,
            limite=20,
        ),
        "assistencias": ranking(
            lambda j: (j["assistencias"], j["gols"]),
            filtro=lambda j: j["assistencias"] > 0,
            limite=20,
        ),
        "melhores_notas": ranking(
            lambda j: (j["nota_media"], j["melhor_nota"], j["melhor_em_campo"]),
            filtro=lambda j: j["partidas"] > 0,
            limite=20,
        ),
        "clean_sheets": ranking(
            lambda j: (j["clean_sheets"], j["nota_media"]),
            filtro=lambda j: j["posicao"] == "Goleiro" and j["clean_sheets"] > 0,
            limite=20,
        ),
        "hat_tricks": ranking(
            lambda j: j["hat_tricks"],
            filtro=lambda j: j["hat_tricks"] > 0,
            limite=20,
        ),
        "mvp": mvp_lista[0] if mvp_lista else None,
        "historico": historico,
        "recordes": _recordes(partidas),
        "evolucao": _evolucao_pontos(partidas, clubes_ordenados),
    }


# ---------------------------------------------------------------------------
# API pública do serviço
# ---------------------------------------------------------------------------

def simular_temporada(seed=None):
    """Roda a temporada e devolve a visão. Não persiste nada."""
    return _montar_visao(_serializar(_rodar(seed), seed))


def salvar_temporada(seed=None):
    """Roda a temporada, grava no banco e devolve o id da simulação."""
    cru = _serializar(_rodar(seed), seed)

    conn = conectar()
    try:
        with conn:
            sim_id = simulacao_repo.criar(
                conn,
                seed=seed,
                campeao=cru["campeao"],
                rodadas=cru["rodadas"],
                criada_em=datetime.now(timezone.utc).isoformat(),
            )
            mapa = clube_repo.inserir(conn, sim_id, cru["clubes"])
            mapa_jog = jogador_repo.inserir(conn, sim_id, mapa, cru["jogadores"])
            partida_ids = partida_repo.inserir(conn, sim_id, mapa, cru["partidas"])
            lance_repo.inserir(
                conn, partida_ids, mapa, mapa_jog, cru["partidas"]
            )
            atuacao_repo.inserir(
                conn, partida_ids, mapa, mapa_jog, cru["partidas"]
            )
        return sim_id
    finally:
        conn.close()


def listar_simulacoes():
    conn = conectar()
    try:
        return [dict(r) for r in simulacao_repo.listar(conn)]
    finally:
        conn.close()


def apagar_simulacao(simulacao_id):
    conn = conectar()
    try:
        with conn:
            return simulacao_repo.deletar(conn, simulacao_id)
    finally:
        conn.close()


def _cru_do_banco(conn, simulacao_id):
    sim = simulacao_repo.buscar(conn, simulacao_id)
    if sim is None:
        return None

    # mantém `id` (o frontend usa para montar os links), descarta as FKs
    clubes = [
        {k: r[k] for k in r.keys() if k != "simulacao_id"}
        for r in clube_repo.listar_por_simulacao(conn, simulacao_id)
    ]

    jogadores = [
        {k: r[k] for k in r.keys() if k not in ("simulacao_id", "clube_id")}
        for r in jogador_repo.listar_por_simulacao(conn, simulacao_id)
    ]

    partidas = [
        {
            "id": r["id"],
            "rodada": r["rodada"],
            "mandante": r["mandante_nome"],
            "visitante": r["visitante_nome"],
            "gols_mandante": r["gols_mandante"],
            "gols_visitante": r["gols_visitante"],
            "posse_mandante": r["posse_mandante"],
            "finalizacoes_mandante": r["finalizacoes_mandante"],
            "finalizacoes_visitante": r["finalizacoes_visitante"],
        }
        for r in partida_repo.listar_por_simulacao(conn, simulacao_id)
    ]

    return {
        "seed": sim["seed"],
        "campeao": sim["campeao"],
        "rodadas": sim["rodadas"],
        "clubes": clubes,
        "jogadores": jogadores,
        "partidas": partidas,
    }


def carregar_temporada(simulacao_id):
    """Lê a simulação do banco e devolve a visão. None se não existir."""
    conn = conectar()
    try:
        cru = _cru_do_banco(conn, simulacao_id)
        return _montar_visao(cru) if cru is not None else None
    finally:
        conn.close()


def detalhe_clube(simulacao_id, clube_id):
    """Clube + elenco + tabela de jogos. None se o clube não for da simulação."""
    conn = conectar()
    try:
        clube = clube_repo.buscar(conn, clube_id)
        if clube is None or clube["simulacao_id"] != simulacao_id:
            return None

        elenco = [
            {k: r[k] for k in r.keys() if k not in ("simulacao_id", "clube_id")}
            for r in jogador_repo.listar_por_clube(conn, clube_id)
        ]

        jogos = []
        for p in partida_repo.listar_por_clube(conn, clube_id):
            em_casa = p["mandante_id"] == clube_id
            pro = p["gols_mandante"] if em_casa else p["gols_visitante"]
            contra = p["gols_visitante"] if em_casa else p["gols_mandante"]
            jogos.append({
                "partida_id": p["id"],
                "rodada": p["rodada"],
                "adversario": p["visitante_nome"] if em_casa else p["mandante_nome"],
                "mando": "casa" if em_casa else "fora",
                "gols_pro": pro,
                "gols_contra": contra,
                "resultado": "V" if pro > contra else "D" if pro < contra else "E",
            })

        c = dict(clube)
        c["saldo_gols"] = c["gols_marcados"] - c["gols_sofridos"]

        return {"clube": c, "elenco": elenco, "jogos": jogos}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# navegação por partida / jogador (fase 2b)
# ---------------------------------------------------------------------------

def _atuacao_visao(r):
    return {
        "jogador_id": r["jogador_id"],
        "jogador": r["jogador_nome"],
        "posicao": r["jogador_posicao"],
        "titular": bool(r["titular"]),
        "entrou_min": r["entrou_min"],
        "saiu_min": r["saiu_min"],
        "gols": r["gols"],
        "assistencias": r["assistencias"],
        "nota": r["nota"],
    }


def detalhe_partida(simulacao_id, partida_id):
    """Placar, estatísticas, timeline e as duas escalações (com nota) de uma
    partida. None se a partida não for da simulação."""

    conn = conectar()
    try:
        p = partida_repo.buscar(conn, partida_id)
        if p is None or p["simulacao_id"] != simulacao_id:
            return None

        eventos = [
            {
                "minuto": r["minuto"],
                "tipo": r["tipo"],
                "jogador": r["jogador_nome"],
                "jogador_id": r["jogador_id"],
                "clube": r["clube_nome"],
                "detalhe": r["detalhe"],
            }
            for r in lance_repo.listar_por_partida(conn, partida_id)
        ]

        atuacoes = atuacao_repo.listar_por_partida(conn, partida_id)
        mandante = [
            _atuacao_visao(r) for r in atuacoes if r["clube_id"] == p["mandante_id"]
        ]
        visitante = [
            _atuacao_visao(r) for r in atuacoes if r["clube_id"] == p["visitante_id"]
        ]

        partida = {
            "id": p["id"],
            "rodada": p["rodada"],
            "mandante": {"id": p["mandante_id"], "nome": p["mandante_nome"]},
            "visitante": {"id": p["visitante_id"], "nome": p["visitante_nome"]},
            "gols_mandante": p["gols_mandante"],
            "gols_visitante": p["gols_visitante"],
            "posse_mandante": p["posse_mandante"],
            "posse_visitante": 100 - p["posse_mandante"],
            "finalizacoes_mandante": p["finalizacoes_mandante"],
            "finalizacoes_visitante": p["finalizacoes_visitante"],
        }

        return {
            "partida": partida,
            "eventos": eventos,
            "escalacao_mandante": mandante,
            "escalacao_visitante": visitante,
        }
    finally:
        conn.close()


def game_log_jogador(simulacao_id, jogador_id):
    """Ficha do jogador + uma linha por partida disputada (nota, contribuição,
    contexto). None se o jogador não for da simulação."""

    conn = conectar()
    try:
        j = jogador_repo.buscar(conn, jogador_id)
        if j is None or j["simulacao_id"] != simulacao_id:
            return None

        jogos = []
        for r in atuacao_repo.listar_por_jogador(conn, jogador_id):
            em_casa = r["mandante_id"] == j["clube_id"]
            pro = r["gols_mandante"] if em_casa else r["gols_visitante"]
            contra = r["gols_visitante"] if em_casa else r["gols_mandante"]
            jogos.append({
                "partida_id": r["partida_id"],
                "rodada": r["rodada"],
                "adversario": r["visitante_nome"] if em_casa else r["mandante_nome"],
                "mando": "casa" if em_casa else "fora",
                "gols_pro": pro,
                "gols_contra": contra,
                "resultado": "V" if pro > contra else "D" if pro < contra else "E",
                "titular": bool(r["titular"]),
                "entrou_min": r["entrou_min"],
                "saiu_min": r["saiu_min"],
                "gols": r["gols"],
                "assistencias": r["assistencias"],
                "nota": r["nota"],
            })

        jogador = {
            "id": j["id"],
            "nome": j["nome"],
            "clube": j["clube"],
            "clube_id": j["clube_id"],
            "posicao": j["posicao"],
            "overall": j["overall"],
            "idade": j["idade"],
            "partidas": j["partidas"],
            "gols": j["gols"],
            "assistencias": j["assistencias"],
            "nota_media": j["nota_media"],
            "melhor_nota": j["melhor_nota"],
            "pior_nota": j["pior_nota"],
            "melhor_em_campo": j["melhor_em_campo"],
        }

        return {"jogador": jogador, "jogos": jogos}
    finally:
        conn.close()
