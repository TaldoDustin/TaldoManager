"""Acesso à tabela `jogador` (snapshot de um jogador dentro de uma simulação)."""

CAMPOS = (
    "nome", "posicao", "idade", "overall", "partidas", "gols", "assistencias",
    "nota_media", "melhor_nota", "pior_nota", "melhor_em_campo",
    "clean_sheets", "hat_tricks", "amarelos", "vermelhos",
)


def inserir(conn, simulacao_id, mapa_clubes, jogadores):
    """`jogadores` são dicts com os CAMPOS + a chave "clube" (nome do clube)."""

    conn.executemany(
        f"""
        INSERT INTO jogador (simulacao_id, clube_id, {", ".join(CAMPOS)})
        VALUES (?, ?, {", ".join("?" * len(CAMPOS))})
        """,
        [
            (simulacao_id, mapa_clubes[j["clube"]], *(j[c] for c in CAMPOS))
            for j in jogadores
        ],
    )


# traz o nome do clube junto (a visão e o frontend usam "clube")
_SELECT = """
    SELECT j.*, c.nome AS clube
    FROM jogador j
    JOIN clube c ON c.id = j.clube_id
"""


def listar_por_simulacao(conn, simulacao_id):
    return conn.execute(
        _SELECT + " WHERE j.simulacao_id = ?", (simulacao_id,)
    ).fetchall()


def listar_por_clube(conn, clube_id):
    return conn.execute(
        _SELECT + " WHERE j.clube_id = ? ORDER BY j.nota_media DESC",
        (clube_id,),
    ).fetchall()


def buscar(conn, jogador_id):
    return conn.execute(
        _SELECT + " WHERE j.id = ?", (jogador_id,)
    ).fetchone()
