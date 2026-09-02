"""Acesso à tabela `simulacao`."""


def criar(conn, seed, campeao, rodadas, criada_em,
          clube_usuario=None, tatica=None, formacao=None, xi_preferido=None):
    cur = conn.execute(
        """
        INSERT INTO simulacao
            (seed, criada_em, campeao, rodadas,
             clube_usuario, tatica, formacao, xi_preferido)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (seed, criada_em, campeao, rodadas,
         clube_usuario, tatica, formacao, xi_preferido),
    )
    return cur.lastrowid


def listar(conn):
    return conn.execute(
        "SELECT * FROM simulacao ORDER BY criada_em DESC, id DESC"
    ).fetchall()


def buscar(conn, simulacao_id):
    return conn.execute(
        "SELECT * FROM simulacao WHERE id = ?", (simulacao_id,)
    ).fetchone()


def deletar(conn, simulacao_id):
    cur = conn.execute("DELETE FROM simulacao WHERE id = ?", (simulacao_id,))
    return cur.rowcount > 0
