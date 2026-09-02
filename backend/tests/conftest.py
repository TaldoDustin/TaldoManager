"""Cada teste roda contra um SQLite temporário e vazio, nunca o banco real."""

import pytest

from app.db.conexao import init_db


@pytest.fixture(autouse=True)
def banco_temporario(tmp_path, monkeypatch):
    monkeypatch.setenv("TALDO_DB", str(tmp_path / "teste.db"))
    init_db()
    yield
