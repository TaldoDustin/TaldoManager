import random

from jogadores import Jogador
from clubes import Clube
from partidas import Partida
from campeonatos import Campeonato

j1 = Jogador("John Doe", 25, "Atacante", 85)
j2 = Jogador("Jane Smith", 28, "Meio-Campo", 88)
j3 = Jogador("Bob Johnson", 30, "Defesa", 82)
j4 = Jogador("Alice Brown", 22, "Goleiro", 80)
j5 = Jogador("Charlie Davis", 27, "Atacante", 90)
j6 = Jogador("Emily Wilson", 24, "Meio-Campo", 87)
j7 = Jogador("David Lee", 29, "Defesa", 83)
j8 = Jogador("Sophia Taylor", 26, "Goleiro", 81)
j9 = Jogador("Michael Miller", 31, "Atacante", 89)
j10 = Jogador("Olivia Anderson", 23, "Meio-Campo", 86)
j11 = Jogador("James Thomas", 27, "Defesa", 84)
j12 = Jogador("Isabella Martinez", 24, "Goleiro", 82)

c1 = Clube("FC Taldo", "Brasil", 1000000)
c2 = Clube("Real Taldo", "Espanha", 2000000)
c3 = Clube("Taldo United", "Inglaterra", 1500000)
c4 = Clube("Taldo City", "Itália", 1200000)

clubes = [c1, c2, c3, c4]

c1.contratar_jogador(j1)
c1.contratar_jogador(j2)
c1.contratar_jogador(j3)

c2.contratar_jogador(j4)
c2.contratar_jogador(j5)
c2.contratar_jogador(j6)

c3.contratar_jogador(j7)
c3.contratar_jogador(j8)
c3.contratar_jogador(j9)

c4.contratar_jogador(j10)
c4.contratar_jogador(j11)
c4.contratar_jogador(j12)


print("=== TALDO MANAGER ===")

campeonato = Campeonato("Campeonato Taldo", clubes)
campeonato.jogar_rodada()
