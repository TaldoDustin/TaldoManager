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
    """Cria as tabelas se não existirem. Idempotente."""

    proprio = conn is None
    conn = conn or conectar()

    try:
        conn.executescript(_SCHEMA.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        if proprio:
            conn.close()
