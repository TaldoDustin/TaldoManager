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


def test_migracao_adiciona_colunas_de_temporada_em_andamento(tmp_path, monkeypatch):
    import sqlite3

    caminho = tmp_path / "antigo.db"
    monkeypatch.setenv("TALDO_DB", str(caminho))

    # simula um banco antigo: tabela simulacao sem as colunas novas
    velho = sqlite3.connect(caminho)
    velho.execute(
        "CREATE TABLE simulacao (id INTEGER PRIMARY KEY, seed INTEGER, "
        "criada_em TEXT NOT NULL, campeao TEXT NOT NULL, rodadas INTEGER NOT NULL)"
    )
    velho.execute(
        "INSERT INTO simulacao (seed, criada_em, campeao, rodadas) "
        "VALUES (1, '2026-01-01', 'FC Taldo', 38)"
    )
    velho.commit()
    velho.close()

    init_db()

    conn = conectar()
    try:
        colunas = {r["name"] for r in conn.execute("PRAGMA table_info(simulacao)")}
        assert {"estado", "rodada_atual", "estado_json"} <= colunas

        linha = conn.execute("SELECT * FROM simulacao WHERE id = 1").fetchone()
        assert linha["estado"] == "concluida"
        assert linha["rodada_atual"] is None
    finally:
        conn.close()
