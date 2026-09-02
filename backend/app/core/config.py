"""Configuração central da aplicação."""

import os
from pathlib import Path

# .../backend/app/core/config.py -> .../backend
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

_DB_PADRAO = BACKEND_DIR / "data" / "database" / "taldo_manager.db"


def caminho_banco():
    """Caminho do SQLite. Sobrescrevível por env (útil em teste)."""
    return os.environ.get("TALDO_DB", str(_DB_PADRAO))
