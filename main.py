import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import carregar_campeonato

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