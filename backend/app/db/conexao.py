"""Conexão com o SQLite e criação do schema."""

import sqlite3
from pathlib import Path

from app.core.config import caminho_banco

_SCHEMA = Path(__file__).with_name("schema.sql")


def conectar():
    """Abre uma conexão com `row_factory` (linhas viram dict-like) e as
    foreign keys ligadas — o SQLite deixa desligado por padrão."""

    caminho = caminho_banco()

    if caminho != ":memory:":
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn=None):
    """Cria as tabelas se não existirem e aplica as migrações. Idempotente."""

    proprio = conn is None
    conn = conn or conectar()

    try:
        conn.executescript(_SCHEMA.read_text(encoding="utf-8"))
        _migrar(conn)
        conn.commit()
    finally:
        if proprio:
            conn.close()


# colunas adicionadas depois do schema inicial — o SQLite não tem
# "ALTER TABLE ... ADD COLUMN IF NOT EXISTS", então a gente checa antes
_COLUNAS_NOVAS = {
    "simulacao": (
        ("clube_usuario", "TEXT"),
        ("tatica", "TEXT"),
        ("formacao", "TEXT"),
        ("xi_preferido", "TEXT"),
    ),
}


def _migrar(conn):
    for tabela, colunas in _COLUNAS_NOVAS.items():
        existentes = {
            r["name"] for r in conn.execute(f"PRAGMA table_info({tabela})")
        }
        for nome, tipo in colunas:
            if nome not in existentes:
                conn.execute(
                    f"ALTER TABLE {tabela} ADD COLUMN {nome} {tipo}"
                )
