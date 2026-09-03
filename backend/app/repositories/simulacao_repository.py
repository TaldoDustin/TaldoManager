"""Acesso à tabela `simulacao`."""


def criar(conn, seed, campeao, rodadas, criada_em,
          clube_usuario=None, tatica=None, formacao=None, xi_preferido=None,
          estado="concluida", rodada_atual=None, estado_json=None):
    cur = conn.execute(
        """
        INSERT INTO simulacao
            (seed, criada_em, campeao, rodadas,
             clube_usuario, tatica, formacao, xi_preferido,
             estado, rodada_atual, estado_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (seed, criada_em, campeao, rodadas,
         clube_usuario, tatica, formacao, xi_preferido,
         estado, rodada_atual, estado_json),
    )
    return cur.lastrowid


def atualizar_estado(conn, simulacao_id, *, estado, rodada_atual,
                     estado_json, campeao, tatica=None, formacao=None,
                     xi_preferido=None):
    """Avança (ou encerra) uma temporada em andamento. `tatica`/`formacao`/
    `xi_preferido` refletem a escolha do técnico para a rodada recém-jogada."""
    conn.execute(
        """
        UPDATE simulacao
           SET estado = ?, rodada_atual = ?, estado_json = ?, campeao = ?,
               tatica = ?, formacao = ?, xi_preferido = ?
         WHERE id = ?
        """,
        (estado, rodada_atual, estado_json, campeao,
         tatica, formacao, xi_preferido, simulacao_id),
    )


def listar(conn):
    # sem `estado_json` — o blob não interessa numa listagem
    return conn.execute(
        """
        SELECT id, seed, criada_em, campeao, rodadas, clube_usuario,
               tatica, formacao, xi_preferido, estado, rodada_atual
        FROM simulacao
        ORDER BY criada_em DESC, id DESC
        """
    ).fetchall()


def buscar(conn, simulacao_id):
    return conn.execute(
        "SELECT * FROM simulacao WHERE id = ?", (simulacao_id,)
    ).fetchone()


def deletar(conn, simulacao_id):
    cur = conn.execute("DELETE FROM simulacao WHERE id = ?", (simulacao_id,))
    return cur.rowcount > 0
