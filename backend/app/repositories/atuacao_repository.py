"""Acesso à tabela `atuacao` (nota e escalação de um jogador por partida)."""


def inserir(conn, partida_ids, mapa_clubes, mapa_jogadores, partidas):
    """`partida_ids` alinhado com `partidas`; cada partida tem a chave
    "atuacoes" (dicts com jogador/clube/titular/entrou_min/saiu_min/...)."""

    linhas = []
    for partida_id, p in zip(partida_ids, partidas):
        for a in p["atuacoes"]:
            linhas.append((
                partida_id,
                mapa_jogadores[(a["clube"], a["jogador"])],
                mapa_clubes[a["clube"]],
                int(a["titular"]),
                a["entrou_min"],
                a["saiu_min"],
                a["gols"],
                a["assistencias"],
                a["nota"],
            ))

    conn.executemany(
        """
        INSERT INTO atuacao
            (partida_id, jogador_id, clube_id, titular,
             entrou_min, saiu_min, gols, assistencias, nota)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        linhas,
    )


def listar_por_partida(conn, partida_id):
    return conn.execute(
        """
        SELECT
            a.*,
            j.nome    AS jogador_nome,
            j.posicao AS jogador_posicao,
            j.overall AS jogador_overall,
            c.nome    AS clube_nome
        FROM atuacao a
        JOIN jogador j ON j.id = a.jogador_id
        JOIN clube   c ON c.id = a.clube_id
        WHERE a.partida_id = ?
        ORDER BY a.titular DESC, a.nota DESC
        """,
        (partida_id,),
    ).fetchall()


def listar_por_jogador(conn, jogador_id):
    """Game log: uma linha por partida em que o jogador atuou, com o contexto
    da partida (rodada, adversário, placar) já resolvido."""

    return conn.execute(
        """
        SELECT
            a.*,
            p.id             AS partida_id,
            p.rodada         AS rodada,
            p.mandante_id    AS mandante_id,
            p.visitante_id   AS visitante_id,
            p.gols_mandante  AS gols_mandante,
            p.gols_visitante AS gols_visitante,
            m.nome           AS mandante_nome,
            v.nome           AS visitante_nome
        FROM atuacao a
        JOIN partida p ON p.id = a.partida_id
        JOIN clube   m ON m.id = p.mandante_id
        JOIN clube   v ON v.id = p.visitante_id
        WHERE a.jogador_id = ?
        ORDER BY p.rodada, p.id
        """,
        (jogador_id,),
    ).fetchall()
