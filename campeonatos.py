import random

from partidas import Partida

class Campeonato:
    def __init__(self, nome, clubes):
        self.nome = nome
        self.clubes = clubes
        
    def jogar_rodada(self):
        print(f"Jogando rodada do campeonato {self.nome}...\n")
        # Simula partidas entre os clubes
        random.shuffle(self.clubes)
        for i in range(0, len(self.clubes), 2):
            if i + 1 < len(self.clubes):
                partida = Partida(self.clubes[i], self.clubes[i + 1])
                partida.simular_partida()