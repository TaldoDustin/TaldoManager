"""Acesso à tabela `clube` (snapshot de um clube dentro de uma simulação)."""

CAMPOS = (
    "nome", "pais", "posicao_final", "pontos", "jogos",
    "vitorias", "empates", "derrotas", "gols_marcados", "gols_sofridos",
)


def inserir(conn, simulacao_id, clubes):
    """Insere os clubes e devolve um mapa {nome: id} para ligar jogadores
    e partidas."""

    mapa = {}
    for clube in clubes:
        cur = conn.execute(
            f"""
            INSERT INTO clube (simulacao_id, {", ".join(CAMPOS)})
            VALUES (?, {", ".join("?" * len(CAMPOS))})
            """,
            (simulacao_id, *(clube[c] for c in CAMPOS)),
        )
        mapa[clube["nome"]] = cur.lastrowid

    return mapa


def listar_por_simulacao(conn, simulacao_id):
    return conn.execute(
        "SELECT * FROM clube WHERE simulacao_id = ? ORDER BY posicao_final",
        (simulacao_id,),
    ).fetchall()


def buscar(conn, clube_id):
    return conn.execute(
        "SELECT * FROM clube WHERE id = ?", (clube_id,)
    ).fetchone()
