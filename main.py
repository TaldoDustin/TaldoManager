import random

from jogadores import Jogador
from clubes import Clube
from partidas import Partida

j1 = Jogador("John Doe", 25, "Atacante", 85)
j2 = Jogador("Jane Smith", 28, "Meio-Campo", 88)
j3 = Jogador("Bob Johnson", 30, "Defesa", 82)
j4 = Jogador("Alice Brown", 22, "Goleiro", 80)
j5 = Jogador("Charlie Davis", 27, "Atacante", 90)
j6 = Jogador("Emily Wilson", 24, "Meio-Campo", 87)

c1 = Clube("FC Taldo", "Brasil", 1000000)
c2 = Clube("Real Taldo", "Espanha", 2000000)

clubes = [c1, c2]

c1.contratar_jogador(j1)
c1.contratar_jogador(j2)
c1.contratar_jogador(j3)

c2.contratar_jogador(j4)
c2.contratar_jogador(j5)
c2.contratar_jogador(j6)




print("=== TALDO MANAGER ===")

print("\n=== Partida ===")
p1= Partida(c1, c2)
p1.simular_partida()
