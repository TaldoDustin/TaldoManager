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
        
        if jogador.posicao == "Atacante":
            peso = 5.0
        elif jogador.posicao == "Meio-campista":
            peso = 3.0
        elif jogador.posicao == "Defensor":
            peso = 1.0
        else:
            peso = 0.2

        for _ in range(self.gols_c1):
            jogador = random.choice(self.clube1.jogadores)
            jogador.gols += peso
        
        for _ in range(self.gols_c2):
            jogador = random.choice(self.clube2.jogadores)
            jogador.gols += peso

        if self.gols_c1 > self.gols_c2:
            self.resultado = f"{self.clube1.nome} venceu!"
        elif self.gols_c2 > self.gols_c1:
            self.resultado = f"{self.clube2.nome} venceu!"      
        else:
            self.resultado = "Empate!"

        
        print(f"{self.clube1.nome} {self.gols_c1} x {self.gols_c2} {self.clube2.nome}")
        print(f"{self.resultado}\n")
        
        if self.gols_c1 > self.gols_c2:
            self.clube1.pontos += 3
            self.clube1.vitorias += 1
            self.clube2.derrotas += 1
        elif self.gols_c2 > self.gols_c1:
            self.clube2.pontos += 3
            self.clube2.vitorias += 1
            self.clube1.derrotas += 1
        else:
            self.clube1.pontos += 1
            self.clube2.pontos += 1
            self.clube1.empates += 1
            self.clube2.empates += 1
            
        self.clube1.gols_marcados += self.gols_c1
        self.clube1.gols_sofridos += self.gols_c2   
        self.clube2.gols_marcados += self.gols_c2
        self.clube2.gols_sofridos += self.gols_c1

    def gerar_gols(self):

    # Força base dos clubes
        forca_c1 = self.clube1.calcular_forca()
        forca_c2 = self.clube2.calcular_forca()

    # Dia bom / dia ruim
        forca_c1 += random.randint(-1, 1)
        forca_c2 += random.randint(-1, 1)

        diferenca = forca_c1 - forca_c2
        diferenca_abs = abs(diferenca)

    # Chance inicial de vitória
        chance_c1 = 0.5 + (diferenca * 0.07)

    # Limites
        chance_c1 = max(0.15, min(0.85, chance_c1))
        chance_c2 = 1 - chance_c1

    # Empate dinâmico
        if diferenca_abs <= 2:
            chance_empate = 0.20

        elif diferenca_abs <= 5:
            chance_empate = 0.18

        elif diferenca_abs <= 8:
            chance_empate = 0.12

        else:
            chance_empate = 0.08

    # Redistribui as chances restantes
        total = chance_c1 + chance_c2

        chance_c1 = (chance_c1 / total) * (1 - chance_empate)
        chance_c2 = (chance_c2 / total) * (1 - chance_empate)

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

        print(f"Chance empate: {chance_empate:.1%}")
        print("--------------------------")

    # Define o tamanho dos placares
        sorteio = random.random()

        if diferenca_abs <= 2:

            vitorias = [
                (1,0),
                (2,1),
                (1,0),
                (2,1),
                (3,2)
            ]       

            empates = [
                (0,0),
                (1,1),
                (1,1),
                (2,2)
            ]

        elif diferenca_abs <= 6:

            vitorias = [
                (1,0),
                (2,0),
                (2,1),
                (3,1),
                (3,0)
            ]

            empates = [
                (0,0),
                (1,1),
                (2,2)
            ]

        else:

            vitorias = [
                (1,0),
                (2,0),
                (2,0),
                (2,1),
                (3,0),
                (3,1),
                (4,0),
                (4,1)
            ]

            empates = [
                (0,0),
                (1,1)
            ]


        if sorteio < chance_c1:

            gols_c1, gols_c2 = random.choice(vitorias)

        elif sorteio < chance_c1 + chance_empate:

            gols_c1, gols_c2 = random.choice(empates)

        else:

            gols_c2, gols_c1 = random.choice(vitorias)
        
        return gols_c1, gols_c2