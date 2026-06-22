import random

from partidas import Partida

class Campeonato:
    def __init__(self, nome, clubes):
        self.nome = nome
        self.clubes = clubes
        self.rodada = 1
        self.historico = []
        self.partidas_jogadas = []
        
    def jogar_rodada(self):
        print(f"Jogando rodada do campeonato {self.nome}...\n")

        print("=" * 40)
        print(f"Rodada {self.rodada}")
        print("=" * 40)

        random.shuffle(self.clubes)

        for i in range(0, len(self.clubes), 2):

            if i + 1 < len(self.clubes):

                confronto = frozenset([
                    self.clubes[i].nome,
                    self.clubes[i + 1].nome
                ])

            if confronto not in self.partidas_jogadas:

                partida = Partida(
                    self.clubes[i],
                    self.clubes[i + 1]
                )

                partida.simular_partida()

                self.partidas_jogadas.append(confronto)

                self.historico.append(
                    f"Rodada {self.rodada}: "
                    f"{partida.clube1.nome} {partida.gols_c1} x "
                    f"{partida.gols_c2} {partida.clube2.nome}"
                )

        self.rodada += 1
        

    def mostrar_classificacao(self):
        print(f"Classificação do campeonato {self.nome}:")
        classificacao = sorted(self.clubes, key=lambda c: (c.pontos, c.saldo_gols(), c.gols_marcados), reverse=True)
        for idx, clube in enumerate(classificacao, start=1):
            jogos = clube.vitorias + clube.empates + clube.derrotas
            print(
                f"{idx}. {clube.nome} | "
                f"P: {clube.pontos} | "
                f"J: {jogos} | "
                f"V: {clube.vitorias} | "
                f"E: {clube.empates} | "
                f"D: {clube.derrotas} | "
                f"GP: {clube.gols_marcados} | "
                f"GC: {clube.gols_sofridos} | "
                f"SG: {clube.saldo_gols()}"
            )
   
    def mostrar_historico(self):
        print(f"Histórico do campeonato {self.nome}:")
        for evento in self.historico:
            print(f"- {evento}")        