"""Roda uma temporada completa direto no terminal (modo CLI).

Uso (a partir da pasta backend/):
    python -m scripts.simular
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from scripts.data_loader import carregar_campeonato


def main():
    campeonato = carregar_campeonato()

    print("=== TALDO MANAGER ===")

    while campeonato.rodada <= len(campeonato.calendario):
        campeonato.jogar_rodada()

    campeonato.mostrar_classificacao()
    campeonato.mostrar_historico()
    campeonato.mostrar_artilharia()
    campeonato.melhores_notas()
    campeonato.assistencias()
    campeonato.clean_sheets()
    campeonato.mvp_campeonato()
    campeonato.mostrar_recordes()


if __name__ == "__main__":
    main()
