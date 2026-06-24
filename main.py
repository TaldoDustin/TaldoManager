import random

from jogadores import Jogador
from clubes import Clube
from partidas import Partida
from campeonatos import Campeonato

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



c1 = Clube("FC Taldo", "Brasil", 1000000, 0)
c2 = Clube("Real Taldo", "Espanha", 2000000, 0)
c3 = Clube("Taldo United", "Inglaterra", 1500000, 0)
c4 = Clube("Taldo City", "Itália", 1200000, 0)

clubes = [c1, c2, c3, c4]

c1.contratar_jogador(j1)
c1.contratar_jogador(j2)
c1.contratar_jogador(j3)
c1.contratar_jogador(j4)

c2.contratar_jogador(j5)
c2.contratar_jogador(j6)
c2.contratar_jogador(j7)
c2.contratar_jogador(j8)

c3.contratar_jogador(j9)
c3.contratar_jogador(j10)
c3.contratar_jogador(j11)
c3.contratar_jogador(j12)

c4.contratar_jogador(j13)
c4.contratar_jogador(j14)
c4.contratar_jogador(j15)
c4.contratar_jogador(j16)


print("=== TALDO MANAGER ===")

campeonato = Campeonato("Taldo", clubes)
campeonato.jogar_rodada()
campeonato.jogar_rodada()
campeonato.jogar_rodada()
campeonato.jogar_rodada()
campeonato.jogar_rodada()
campeonato.jogar_rodada()

campeonato.mostrar_classificacao()
campeonato.mostrar_historico()
campeonato.mostrar_artilharia()

campeonato.melhores_notas()
campeonato.assistencias()
j14.mostrar_estatisticas()

