class Partida:
    def __init__(self, clube1, clube2):
        self.clube1 = clube1
        self.clube2 = clube2
        self.resultado = None
        
    def simular_partida(self):
        forca_c1 = self.clube1.calcular_forca()
        forca_c2 = self.clube2.calcular_forca()

        if forca_c1 > forca_c2:
            self.resultado = f"{self.clube1.nome} venceu"

        elif forca_c2 > forca_c1:
            self.resultado = f"{self.clube2.nome} venceu"

        else:
            self.resultado = "Empate"

        print(self.resultado)