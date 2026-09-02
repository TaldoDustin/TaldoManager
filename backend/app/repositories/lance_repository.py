"""Acesso à tabela `lance` (timeline da partida)."""


def inserir(conn, partida_ids, mapa_clubes, mapa_jogadores, partidas):
    """`partida_ids` alinhado com `partidas`; cada partida tem a chave
    "eventos" (dicts com minuto/tipo/clube/jogador/detalhe)."""

    linhas = []
    for partida_id, p in zip(partida_ids, partidas):
        for e in p["eventos"]:
            clube_id = mapa_clubes.get(e["clube"])
            jogador_id = (
                mapa_jogadores.get((e["clube"], e["jogador"]))
                if e["jogador"] is not None
                else None
            )
            linhas.append((
                partida_id, e["minuto"], e["tipo"],
                clube_id, jogador_id, e["detalhe"],
            ))

    conn.executemany(
        """
        INSERT INTO lance
            (partida_id, minuto, tipo, clube_id, jogador_id, detalhe)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        linhas,
    )


def listar_por_partida(conn, partida_id):
    return conn.execute(
        """
        SELECT
            l.*,
            j.nome AS jogador_nome,
            j.id   AS jogador_id,
            c.nome AS clube_nome
        FROM lance l
        LEFT JOIN jogador j ON j.id = l.jogador_id
        LEFT JOIN clube   c ON c.id = l.clube_id
        WHERE l.partida_id = ?
        ORDER BY l.minuto, l.id
        """,
        (partida_id,),
    ).fetchall()
