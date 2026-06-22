import random

class Partida:
    def __init__(self, clube1, clube2):
        self.clube1 = clube1
        self.clube2 = clube2
        self.resultado = None
        
    def simular_partida(self):
        gols_c1, gols_c2 = self.gerar_gols()

        if gols_c1 > gols_c2:
            self.resultado = f"{self.clube1.nome} venceu!"
        elif gols_c2 > gols_c1:
            self.resultado = f"{self.clube2.nome} venceu!"      
        else:
            self.resultado = "Empate!"

        print(self.resultado)
        print(f"Gols: {gols_c1:.0f} - {gols_c2:.0f}")
    
    def gerar_gols(self):
        forca_c1 = self.clube1.calcular_forca()
        forca_c2 = self.clube2.calcular_forca()

        diferenca_forca = forca_c1 - forca_c2
        if diferenca_forca > 5:
            probabilidade_c1 = 0.8 + (diferenca_forca / 100)
            probabilidade_c2 = 0.2 - (diferenca_forca / 100)
        elif diferenca_forca > 2:
            probabilidade_c1 = 0.7 + (diferenca_forca / 100)
            probabilidade_c2 = 0.3 - (diferenca_forca / 100)
        else:
            probabilidade_c1 = 0.5
            probabilidade_c2 = 0.5  
            
        gols_c1 = int(round(random.random() * probabilidade_c1 * 5))
        gols_c2 = int(round(random.random() * probabilidade_c2 * 5))

        return gols_c1, gols_c2