import random
class Partida:
    def __init__(self, clube1, clube2):
        self.clube1 = clube1
        self.clube2 = clube2
        self.resultado = None
        self.gols_c1 = 0
        self.gols_c2 = 0
    
    def simular_partida(self):

        self.gols_c1, self.gols_c2 = self.gerar_gols()

        estatisticas = self.criar_estatisticas()

        self.distribuir_gols(
            self.clube1,
            self.gols_c1,
            estatisticas
        )

        self.distribuir_gols(
            self.clube2,
            self.gols_c2,
            estatisticas
        )

        self.definir_resultado()
        self.mostrar_resultado()

        self.atualizar_classificacao()
        self.atualizar_estatisticas_clubes()

        melhor_jogador, maior_nota = self.calcular_notas(estatisticas)

        self.mostrar_melhor_em_campo(
            melhor_jogador,
            maior_nota
        )    

#distribuição

    def criar_estatisticas(self):

        estatisticas = {}

        for jogador in self.clube1.jogadores + self.clube2.jogadores:
            estatisticas[jogador] = {
                "gols": 0, 
                "assistencias": 0
            }

        return estatisticas
    
    def distribuir_gols(self, clube, quantidade_gols, estatisticas):

        lista = []

        for jogador in clube.jogadores:

            peso = jogador.peso_gol()

            if peso > 0:
                lista.extend([jogador] * peso)

        if not lista:
            return

        for _ in range(quantidade_gols):

            artilheiro = random.choice(lista)

            artilheiro.gols += 1
            estatisticas[artilheiro]["gols"] += 1

            self.distribuir_assistencia(
                clube,
                artilheiro,
                estatisticas
            )

    def distribuir_assistencia(self, clube, artilheiro, estatisticas):

        lista = []

        for jogador in clube.jogadores:

            if jogador != artilheiro:

                peso = jogador.peso_assistencia()

                if peso > 0:
                    lista.extend([jogador] * peso)

        if lista and random.random() < 0.70:

            assistente = random.choice(lista)

            assistente.assistencias += 1
            estatisticas[assistente]["assistencias"] += 1

#resultado

    def definir_resultado(self):

        if self.gols_c1 > self.gols_c2:
            self.resultado = f"{self.clube1.nome} venceu!"

        elif self.gols_c2 > self.gols_c1:
            self.resultado = f"{self.clube2.nome} venceu!"

        else:
            self.resultado = "Empate!"

    def mostrar_resultado(self):

        print(
            f"{self.clube1.nome} "
            f"{self.gols_c1} x "
            f"{self.gols_c2} "
            f"{self.clube2.nome}"
        )

        print(f"{self.resultado}\n")

#campeonato

    def atualizar_classificacao(self):

        if self.gols_c1 > self.gols_c2:

            self.clube1.pontos += 3
            self.clube1.vitorias += 1
            self.clube2.derrotas += 1

            self.clube1.atualizar_forma("V")
            self.clube2.atualizar_forma("D")

        elif self.gols_c2 > self.gols_c1:

            self.clube2.pontos += 3
            self.clube2.vitorias += 1
            self.clube1.derrotas += 1

            self.clube2.atualizar_forma("V")
            self.clube1.atualizar_forma("D")

        else:

            self.clube1.pontos += 1
            self.clube2.pontos += 1

            self.clube1.empates += 1
            self.clube2.empates += 1

            self.clube1.atualizar_forma("E")
            self.clube2.atualizar_forma("E")
            
    def atualizar_estatisticas_clubes(self):

        self.clube1.gols_marcados += self.gols_c1
        self.clube1.gols_sofridos += self.gols_c2

        self.clube2.gols_marcados += self.gols_c2
        self.clube2.gols_sofridos += self.gols_c1   

#jogadores

    def calcular_notas(self, estatisticas):

        melhor_jogador = None
        maior_nota = 0

        for jogador in self.clube1.jogadores + self.clube2.jogadores:

            nota = 6.0

            gols = estatisticas[jogador]["gols"]
            assistencias = estatisticas[jogador]["assistencias"]

            if jogador.posicao == "Atacante":
                bonus_gol = 0.8
                bonus_assistencia = 0.4

            elif jogador.posicao == "Meio-Campo":
                bonus_gol = 0.9
                bonus_assistencia = 0.6

            elif jogador.posicao == "Defesa":
                bonus_gol = 1.0
                bonus_assistencia = 0.7

            else:  # Goleiro
                bonus_gol = 1.5
                bonus_assistencia = 1.0

            nota += gols * bonus_gol
            nota += assistencias * bonus_assistencia

            # Resultado da partida

            if jogador in self.clube1.jogadores:

                if self.gols_c1 > self.gols_c2:
                    nota += 0.3

                elif self.gols_c1 < self.gols_c2:
                    nota -= 0.2

            else:

                if self.gols_c2 > self.gols_c1:
                    nota += 0.3

                elif self.gols_c2 < self.gols_c1:
                    nota -= 0.2

            # Limita entre 0 e 10

            nota = max(0, min(10, nota))

            jogador.soma_nota += nota
            jogador.partidas += 1

            if nota > jogador.melhor_nota:
                jogador.melhor_nota = nota

            if nota < jogador.pior_nota:
                jogador.pior_nota = nota

            # Melhor da partida

            if melhor_jogador is None:

                melhor_jogador = jogador
                maior_nota = nota

            elif (
                nota > maior_nota
                or
                (
                    nota == maior_nota
                    and
                    (
                        estatisticas[jogador]["gols"],
                        estatisticas[jogador]["assistencias"]
                    )
                    >
                    (
                        estatisticas[melhor_jogador]["gols"],
                        estatisticas[melhor_jogador]["assistencias"]
                    )
                )
            ):

                melhor_jogador = jogador
                maior_nota = nota

        melhor_jogador.melhor_em_campo += 1

        return melhor_jogador, maior_nota
    
    def mostrar_melhor_em_campo(self, jogador, nota):

        print("\n⭐ MELHOR EM CAMPO")

        print(
            f"{jogador.nome} " 
            f"({jogador.posicao}) " 
            f"- Nota {nota:.1f}\n")

#simulação

    def gerar_gols(self):

        forca_c1, forca_c2 = self.calcular_forcas()

        (
            chance_c1,
            chance_c2,
            chance_empate,
            diferenca_abs
        ) = self.calcular_probabilidades(
            forca_c1,
            forca_c2
        )

        self.mostrar_analise(
            forca_c1,
            forca_c2,
            chance_c1,
            chance_c2,
            chance_empate
        )

        (
            vitorias_favorito,
            vitorias_azarao,
            empates
        ) = self.definir_placares(
            diferenca_abs
        )

        return self.sortear_resultado(
            chance_c1,
            chance_empate,
            vitorias_favorito,
            vitorias_azarao,
            empates
        )
        
    def calcular_forcas(self):

        forca_c1 = self.clube1.calcular_forca()
        forca_c2 = self.clube2.calcular_forca()

        # vantagem do mandante
        forca_c1 += 1

        # dia bom / ruim
        forca_c1 += random.randint(-1, 1)
        forca_c2 += random.randint(-1, 1)

        return forca_c1, forca_c2
    
    def calcular_probabilidades(
        self,
        forca_c1,
        forca_c2
    ):

        diferenca = forca_c1 - forca_c2
        diferenca_abs = abs(diferenca)

        chance_c1 = 0.5 + (diferenca * 0.06)

        chance_c1 = max(
            0.15,
            min(0.85, chance_c1)
        )

        chance_c2 = 1 - chance_c1

        if diferenca_abs <= 2:
            chance_empate = 0.15

        elif diferenca_abs <= 5:
            chance_empate = 0.12

        elif diferenca_abs <= 8:
            chance_empate = 0.08

        else:
            chance_empate = 0.05

        total = chance_c1 + chance_c2

        chance_c1 = (
            chance_c1 / total
        ) * (1 - chance_empate)

        chance_c2 = (
            chance_c2 / total
        ) * (1 - chance_empate)

        return (
            chance_c1,
            chance_c2,
            chance_empate,
            diferenca_abs
        )
        
    def mostrar_analise(
        self,
        forca_c1,
        forca_c2,
        chance_c1,
        chance_c2,
        chance_empate
    ):

        print("\n--- ANÁLISE DA PARTIDA ---")

        print(
            f"{self.clube1.nome}: "
            f"força {forca_c1:.1f} | "
            f"chance {chance_c1:.1%}"
        )

        print(
            f"{self.clube2.nome}: "
            f"força {forca_c2:.1f} | "
            f"chance {chance_c2:.1%}"
        )

        print(
            f"Chance empate: {chance_empate:.1%}"
        )

        print("--------------------------")
        
    def definir_placares(
        self,
        diferenca_abs
    ):

        if diferenca_abs <= 2:

            vitorias_favorito = [
                (1,0),
                (1,0),
                (1,0),
                (2,1),
                (2,1),
                (2,1),
                (3,2)
            ]

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,1),
                (2,1)
            ]

            empates = [
                (0,0),
                (1,1),
                (1,1),
                (1,1),
                (2,2)
            ]

        elif diferenca_abs <= 6:

            vitorias_favorito = [
                (1,0),
                (1,0),
                (2,0),
                (2,0),
                (2,1),
                (2,1),
                (3,1),
                (3,0)
            ]

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,1),
                (2,1),
                (2,0)
            ]

            empates = [
                (0,0),
                (1,1),
                (1,1),
                (2,2)
            ]

        else:

            vitorias_favorito = [
                (1,0),
                (2,0),
                (2,0),
                (2,0),
                (2,1),
                (3,0),
                (3,1),
                (3,1),
                (4,0),
                (4,1)
            ]

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,0),
                (2,1)
            ]

            empates = [
                (0,0),
                (1,1)
            ]

        if diferenca_abs >= 10:

            vitorias_favorito.extend([
                (2,0),
                (3,0),
                (3,1),
                (4,0),
                (5,0)
            ])

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,0),
                (2,1)
            ]

            empates = [
                (0,0),
                (1,1)
            ]

        return (
            vitorias_favorito,
            vitorias_azarao,
            empates
        )
        
    def sortear_resultado(
        self,
        chance_c1,
        chance_empate,
        vitorias_favorito,
        vitorias_azarao,
        empates
    ):

        sorteio = random.random()

        if sorteio < chance_c1:

            gols_c1, gols_c2 = random.choice(
                vitorias_favorito
            )

        elif sorteio < chance_c1 + chance_empate:

            gols_c1, gols_c2 = random.choice(
                empates
            )

        else:

            gols_c2, gols_c1 = random.choice(
                vitorias_azarao
            )

        return gols_c1, gols_c2