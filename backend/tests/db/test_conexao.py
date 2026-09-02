from app.db.conexao import conectar, init_db


def test_init_db_cria_as_tabelas():
    init_db()  # idempotente — o conftest já chamou uma vez

    conn = conectar()
    try:
        tabelas = {
            r["name"]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
    finally:
        conn.close()

    assert {"simulacao", "clube", "jogador", "partida"} <= tabelas


def test_foreign_keys_ligadas():
    conn = conectar()
    try:
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    finally:
        conn.close()


def test_linhas_vem_como_dict():
    conn = conectar()
    try:
        conn.execute(
            "INSERT INTO simulacao (seed, criada_em, campeao, rodadas) "
            "VALUES (1, '2026-01-01', 'FC Taldo', 38)"
        )
        linha = conn.execute("SELECT * FROM simulacao").fetchone()
        assert linha["campeao"] == "FC Taldo"
        assert linha["seed"] == 1
    finally:
        conn.close()
