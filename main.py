from jogadores import Jogador
from clubes import Clube
from campeonatos import Campeonato

# =========================
# JOGADORES
# =========================

j1 = Jogador("John Doe", 25, "Atacante", 85)
j2 = Jogador("Jane Smith", 28, "Meio-Campo", 88)
j3 = Jogador("Bob Johnson", 30, "Defesa", 82)
j4 = Jogador("Alice Brown", 22, "Goleiro", 90)

j5 = Jogador("Charlie Davis", 27, "Atacante", 90)
j6 = Jogador("Emily Wilson", 24, "Meio-Campo", 90)
j7 = Jogador("David Lee", 29, "Defesa", 83)
j8 = Jogador("Sophia Taylor", 26, "Goleiro", 81)

j9 = Jogador("Michael Miller", 31, "Atacante", 89)
j10 = Jogador("Olivia Anderson", 23, "Meio-Campo", 86)
j11 = Jogador("James Thomas", 27, "Defesa", 84)
j12 = Jogador("Isabella Martinez", 24, "Goleiro", 82)

j13 = Jogador("Juan Soares", 17, "Atacante", 79)
j14 = Jogador("Isaque Souza", 18, "Meio-Campo", 95)
j15 = Jogador("Jhon Alex", 27, "Defesa", 84)
j16 = Jogador("Rafaela Montes", 24, "Goleiro", 83)


# =========================
# CLUBES
# =========================

c1 = Clube("FC Taldo", "Brasil", 1000000, 0)
c2 = Clube("Real Taldo", "Espanha", 2000000, 0)
c3 = Clube("Taldo United", "Inglaterra", 1500000, 0)
c4 = Clube("Taldo City", "Itália", 1200000, 0)

clubes = [c1, c2, c3, c4]


# =========================
# ELENCOS
# =========================

for jogador in [j1, j2, j3, j4]:
    c1.contratar_jogador(jogador)

for jogador in [j5, j6, j7, j8]:
    c2.contratar_jogador(jogador)

for jogador in [j9, j10, j11, j12]:
    c3.contratar_jogador(jogador)

for jogador in [j13, j14, j15, j16]:
    c4.contratar_jogador(jogador)


# =========================
# CAMPEONATO
# =========================

print("=== TALDO MANAGER ===")

campeonato = Campeonato("Taldo", clubes)


# Joga todas as rodadas automaticamente
while campeonato.rodada <= len(campeonato.calendario):
    campeonato.jogar_rodada()


# =========================
# RELATÓRIOS
# =========================

campeonato.mostrar_classificacao()
campeonato.mostrar_historico()

campeonato.mostrar_artilharia()
campeonato.assistencias()
campeonato.melhores_notas()

campeonato.mvp_campeonato()