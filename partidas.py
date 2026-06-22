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

        if self.gols_c1 > self.gols_c2:
            self.resultado = f"{self.clube1.nome} venceu!"
        elif self.gols_c2 > self.gols_c1:
            self.resultado = f"{self.clube2.nome} venceu!"      
        else:
            self.resultado = "Empate!"

        
        print(f"{self.clube1.nome} {self.gols_c1} x {self.gols_c2} {self.clube2.nome}")
        print(f"{self.resultado}\n")
    
    def gerar_gols(self):
        forca_c1 = self.clube1.calcular_forca()
        forca_c2 = self.clube2.calcular_forca()
        
        diferenca = abs(forca_c1 - forca_c2)

        if diferenca <= 2:
            probabilidade_c1 = 0.5
            probabilidade_c2 = 0.5
        elif forca_c1 > forca_c2:
            probabilidade_c1 = 0.6
            probabilidade_c2 = 0.4
        else:
            probabilidade_c1 = 0.4
            probabilidade_c2 = 0.6

        gols_c1 = random.randint(0, 3)
        gols_c2 = random.randint(0, 3)
        if random.random() < probabilidade_c1:
            gols_c1 += 1
        if random.random() < probabilidade_c2:
            gols_c2 += 1

        return gols_c1, gols_c2