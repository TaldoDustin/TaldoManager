import random

import jogadores
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

        if self.rodada > len(self.calendario):
            print("Campeonato encerrado!")
            return

        rodada_atual = self.calendario[self.rodada - 1]

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

        times = self.clubes[:]

        if len(times) % 2 != 0:
            times.append(None)

        rodadas = []

        for _ in range(len(times) - 1):

            rodada = []

            for i in range(len(times) // 2):

                time1 = times[i]
                time2 = times[-i - 1]

                if time1 is not None and time2 is not None:
                    rodada.append((time1, time2))

            rodadas.append(rodada)

            times = (
                [times[0]]
                + [times[-1]]
                + times[1:-1]
            )

        return rodadas
    
    def mostrar_artilharia(self):

        jogadores = []

        for clube in self.clubes:
            jogadores.extend(clube.jogadores)

        artilharia = sorted(
            jogadores,
            key=lambda j: j.gols,
            reverse=True
        )   

        print("\n=== ARTILHARIA ===")

        for jogador in artilharia:
            if jogador.gols > 0:
                print(f"{jogador.nome} - {jogador.gols} gols")