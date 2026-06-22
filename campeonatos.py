import random

from partidas import Partida

class Campeonato:
    def __init__(self, nome, clubes):
        self.nome = nome
        self.clubes = clubes
        self.rodada = 1
        self.historico = []
        self.partidas_jogadas = []
        self.calendario = self.gerar_calendario()
        
    def jogar_rodada(self):

        print(f"\n{'=' * 40}")
        print(f"Rodada {self.rodada}")
        print(f"{'=' * 40}")

        jogos_por_rodada = len(self.clubes) // 2

        inicio = (self.rodada - 1) * jogos_por_rodada
        fim = inicio + jogos_por_rodada

        rodada_atual = self.calendario[inicio:fim]

        if not rodada_atual:
            print("Campeonato encerrado!")
            return

        for clube1, clube2 in rodada_atual:

            partida = Partida(clube1, clube2)
            partida.simular_partida()

            self.historico.append(
                f"Rodada {self.rodada}: "
                f"{clube1.nome} {partida.gols_c1} x "
                f"{partida.gols_c2} {clube2.nome}"
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
            
    def gerar_calendario(self):
        rodadas = []
        for i in range(len(self.clubes)):
            for j in range(i + 1, len(self.clubes)):
                rodadas.append(
                    (self.clubes[i], self.clubes[j])
                )

        return rodadas